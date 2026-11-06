#!/usr/bin/env python3
"""dep_lint: mechanical enforcement of DEP&CC 2.0 for the IGTP repository.

Data-driven: every pattern, threshold, and severity lives in .dep/dep_lint.json.
The linter is lexical and structural. It does not decide mathematical truth;
kernel checking happens in Lean, and Chapter 33.4 lists what remains outside
mechanical reach.

Implemented rules (must equal the `rules` array in the configuration; see
DEP-LINT-DOC-SYNC):
  DEP-LINT-ADMITTED            banned proof-skip tokens in Lean sources (Sev 0)
  DEP-LINT-BANNED-PHRASE       Appendix A + doc-standard phrases in documents (Sev 1)
  DEP-LINT-STATUS-VALUE        claim/completeness statuses in the closed vocabularies (Sev 1)
  DEP-LINT-STATUS-CONTAMINATION a complete node depends only on complete, valid-status nodes (Sev 0)
  DEP-LINT-BLOCK               required ledger fields present on every node (Sev 1)
  DEP-LINT-HYP-DECLARED        every hypothesis referenced by a result is ledgered (Sev 0)
  DEP-LINT-FIDELITY            machine-checked results carry fidelity mappings (Sev 0)
  DEP-LINT-DEGENERACY          degeneracy artifacts exist and meet quota (Sev 1)
  DEP-LINT-AXIOM-DRIFT         extracted axiom sets equal the declared ledger (Sev 0)
  DEP-LINT-GAP-EXPIRY          no expired gaps (Sev 1)
  DEP-LINT-DOC-SYNC            rule catalog matches the configuration (Sev 1)
  DEP-LINT-DOCSTRINGS          every public Lean declaration carries a docstring (Sev 2)
  DEP-LINT-RESULTS-TABLE       dep/out/results_table.md matches regeneration (Sev 1)

Exit codes (Chapter 33.1): 0 no failing findings; 1 failing findings at a
severity in fail_on or failed self-test; 2 bootstrap failure; 3 usage error.

Deterministic: sorted traversal, findings sorted by (file, line, rule,
message); no locale, time, or environment dependence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONFIG = REPO / ".dep" / "dep_lint.json"

RULE_CATALOG = [
    "DEP-LINT-ADMITTED",
    "DEP-LINT-BANNED-PHRASE",
    "DEP-LINT-STATUS-VALUE",
    "DEP-LINT-STATUS-CONTAMINATION",
    "DEP-LINT-BLOCK",
    "DEP-LINT-HYP-DECLARED",
    "DEP-LINT-FIDELITY",
    "DEP-LINT-DEGENERACY",
    "DEP-LINT-AXIOM-DRIFT",
    "DEP-LINT-GAP-EXPIRY",
    "DEP-LINT-DOC-SYNC",
    "DEP-LINT-DOCSTRINGS",
    "DEP-LINT-RESULTS-TABLE",
]


class Finding:
    __slots__ = ("severity", "rule", "file", "line", "message")

    def __init__(self, severity: int, rule: str, file: str, line: int, message: str):
        self.severity = severity
        self.rule = rule
        self.file = file
        self.line = line
        self.message = message

    def key(self):
        return (self.file, self.line, self.rule, self.message)

    def render(self) -> str:
        return f"[Sev {self.severity}] {self.rule} {self.file}:{self.line}: {self.message}"


# ---------------------------------------------------------------------------
# Minimal YAML readers (no external dependency; the ledgers use flat schemas)
# ---------------------------------------------------------------------------


def _strip_comment(line: str) -> str:
    out, in_str = [], False
    for ch in line:
        if ch == '"':
            in_str = not in_str
        if ch == "#" and not in_str:
            break
        out.append(ch)
    return "".join(out).rstrip()


def load_yaml_list(path: Path) -> list[dict]:
    """Parse a flat YAML list of mappings (dep ledgers) without comments.

    Supports both multi-line mappings and single-line inline mappings of the
    form `- {key: value, key: value}`.
    """
    entries, current = [], None
    for raw in path.read_text().splitlines():
        line = _strip_comment(raw)
        if not line.strip() or line.strip() == "---":
            continue
        if re.match(r"^\s*-\s*\{.*\}\s*$", line):
            if current is not None:
                entries.append(current)
            current = {}
            body = line.strip()[2:].strip()
            body = body[1:-1] if body.startswith("{") else body
            for pair in _split_pairs(body):
                m = re.match(r"^([\w.\-]+):\s*(.*)$", pair.strip())
                if m:
                    current[m.group(1)] = _yaml_scalar(m.group(2).strip())
            continue
        if re.match(r"^\s*-\s", line):
            if current is not None:
                entries.append(current)
            current = {}
            line = re.sub(r"^\s*-\s+", "", line)
        if current is None:
            continue
        m = re.match(r"^([\w.\-]+):\s*(.*)$", line.strip())
        if m:
            key, value = m.group(1), m.group(2).strip()
            current[key] = _yaml_scalar(value)
    if current is not None:
        entries.append(current)
    return entries


def _split_pairs(body: str) -> list[str]:
    """Split 'a: 1, b: x, y' on top-level commas (respecting quotes)."""
    pairs, buf, quote, depth = [], [], False, 0
    for ch in body:
        if ch == '"':
            quote = not quote
        if ch in "[{" and not quote:
            depth += 1
        if ch in "]}" and not quote:
            depth -= 1
        if ch == "," and not quote and depth == 0:
            pairs.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        pairs.append("".join(buf))
    return pairs


def _yaml_scalar(value: str):
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [v.strip() for v in _split_pairs(inner)] if inner else []
    if value in {"true", "false"}:
        return value == "true"
    return value


def load_yaml_map(path: Path) -> dict:
    """Parse a flat top-level mapping whose values may be lists or strings."""
    data: dict = {}
    current_key, current_list = None, None
    for raw in path.read_text().splitlines():
        line = _strip_comment(raw)
        if not line.strip() or line.strip() == "---":
            continue
        top = re.match(r"^([\w.\-]+):\s*(.*)$", line)
        if top and not line.startswith((" ", "\t", "-")):
            if current_key is not None and current_list is not None:
                data[current_key] = current_list
                current_list = None
            current_key, value = top.group(1), top.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                data[current_key] = [v.strip() for v in inner.split(",")] if inner else []
            elif value:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                data[current_key] = value
                current_key = None
            else:
                current_list = []
        elif line.strip().startswith("- ") and current_list is not None:
            current_list.append(line.strip()[2:].strip())
    if current_key is not None and current_list is not None:
        data[current_key] = current_list
    return data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def iter_files(base: Path, extensions: list[str], exempt: list[str]) -> list[Path]:
    out = []
    for path in base.rglob("*") if base.is_dir() else [base]:
        if not path.is_file():
            continue
        rel = path.relative_to(REPO).as_posix()
        if any(rel == e or rel.startswith(e.rstrip("/") + "/") for e in exempt):
            continue
        if path.suffix in extensions:
            out.append(path)
    return sorted(out)


def path_in_exempt(rel: str, exempt: list[str]) -> bool:
    return any(rel == e or rel.startswith(e.rstrip("/") + "/") for e in exempt)


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------


def strip_lean_comments(text: str) -> str:
    """Remove Lean block comments (/- ... -/, single level) and -- comments.

    Deterministic lexical preprocessing so that documentation mentioning a
    banned token is not itself a violation; the token scan applies to code.
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("/-", i):
            depth = 1
            j = i + 2
            while j < n and depth:
                if text.startswith("/-", j):
                    depth += 1
                    j += 2
                elif text.startswith("-/", j):
                    depth -= 1
                    j += 2
                else:
                    j += 1
            i = j
            out.append(" ")
        elif text.startswith("--", i):
            while i < n and text[i] != "\n":
                i += 1
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def lean_docstring_lines(text: str) -> set[int]:
    """Map each line index (0-based) to True if it opens a /-- docstring block.

    Returns the set of opening line indices; a declaration immediately after
    a block's closing line is documented iff the block opened with /--.
    """
    lines = text.splitlines()
    docstring_opens: set[int] = set()
    i = 0
    while i < len(lines):
        stripped = lines[i].lstrip()
        if stripped.startswith("/-"):
            is_doc = stripped.startswith("/--")
            start = i
            while i < len(lines) and "-/" not in lines[i]:
                i += 1
            if is_doc:
                docstring_opens.add(start)
        i += 1
    return docstring_opens, len(lines)  # type: ignore[return-value]


def rule_admitted(cfg, findings: list[Finding]) -> None:
    """DEP-LINT-ADMITTED (Sev 0): banned tokens in Lean source code."""
    for base in cfg["lean_scan"]:
        root = REPO / base
        files = iter_files(root, [".lean"], cfg["exempt_paths"])
        for path in files:
            rel = path.relative_to(REPO).as_posix()
            code = strip_lean_comments(path.read_text())
            for lineno, line in enumerate(code.splitlines(), start=1):
                for token in cfg["banned_tokens_lean"]:
                    if token in line:
                        findings.append(Finding(
                            0, "DEP-LINT-ADMITTED", rel, lineno,
                            f"banned token {token.strip()!r} in Lean source"))


def rule_banned_phrase(cfg, findings: list[Finding]) -> None:
    """DEP-LINT-BANNED-PHRASE (Sev 1): Appendix A phrases in documents."""
    word_boundary = set(cfg["banned_phrase_word_boundaries"])
    scan = []
    for entry in cfg["doc_scan"]["paths"]:
        scan.extend(iter_files(REPO / entry, cfg["doc_scan"]["extensions"],
                               cfg["exempt_paths"]))
    for path in scan:
        rel = path.relative_to(REPO).as_posix()
        for lineno, line in enumerate(path.read_text().splitlines(), start=1):
            low = line.lower()
            for phrase in cfg["banned_phrases"]:
                if phrase in word_boundary:
                    if re.search(rf"\b{re.escape(phrase)}\b", low):
                        findings.append(Finding(
                            1, "DEP-LINT-BANNED-PHRASE", rel, lineno,
                            f"banned phrase {phrase!r}"))
                elif phrase in low:
                    findings.append(Finding(
                        1, "DEP-LINT-BANNED-PHRASE", rel, lineno,
                        f"banned phrase {phrase!r}"))


def _load_claims(findings: list[Finding]) -> dict:
    path = REPO / "dep" / "claims.yaml"
    if not path.exists():
        findings.append(Finding(0, "DEP-LINT-BLOCK", "dep/claims.yaml", 0,
                                "claims ledger missing"))
        return {"results": [], "conjectures": [], "empirical": [], "claims": []}
    text = path.read_text()
    sections = {"results": [], "conjectures": [], "empirical": [], "claims": []}
    section = None
    current = None
    for raw in text.splitlines():
        line = _strip_comment(raw)
        m = re.match(r"^(results|conjectures|empirical|claims):\s*$", line)
        if m:
            section = m.group(1)
            continue
        if section is None:
            continue
        if re.match(r"^\s*-\s+id:", line):
            if current:
                sections[section].append(current)
            current = {"id": line.split("id:", 1)[1].strip()}
            continue
        if current is not None:
            km = re.match(r"^\s+([\w.]+):\s*(.*)$", line)
            if km:
                key, value = km.group(1), km.group(2).strip()
                if value.startswith("[") and value.endswith("]"):
                    inner = value[1:-1].strip()
                    value = [v.strip() for v in inner.split(",")] if inner else []
                elif value.startswith("{"):
                    value = value
                current[key] = value
    if current:
        sections[section].append(current)
    return sections


def rule_status_value(cfg, claims, findings: list[Finding]) -> None:
    """DEP-LINT-STATUS-VALUE (Sev 1): closed status vocabularies."""
    statuses = set(cfg["claim_status_vocabulary"])
    completeness = set(cfg["completeness_vocabulary"])
    for section in ("results", "conjectures", "empirical"):
        for node in claims[section]:
            status = str(node.get("claim_status", ""))
            comp = str(node.get("completeness", ""))
            if status not in statuses:
                findings.append(Finding(
                    1, "DEP-LINT-STATUS-VALUE", "dep/claims.yaml", 0,
                    f"{node.get('id')}: claim_status {status!r} outside the closed vocabulary"))
            if comp and comp not in completeness:
                findings.append(Finding(
                    1, "DEP-LINT-STATUS-VALUE", "dep/claims.yaml", 0,
                    f"{node.get('id')}: completeness {comp!r} outside the closed vocabulary"))


def rule_status_contamination(cfg, claims, findings: list[Finding]) -> None:
    """DEP-LINT-STATUS-CONTAMINATION (Sev 0): complete nodes depend only on
    complete nodes with kernel-valid statuses."""
    by_id = {}
    for section in ("results", "conjectures", "empirical"):
        for node in claims[section]:
            by_id[str(node.get("id"))] = node
    ok_statuses = set(cfg["complete_ok_statuses"])
    for node in claims["results"]:
        if str(node.get("completeness")) != "complete":
            continue
        for dep in node.get("depends", []) or []:
            target = by_id.get(str(dep))
            if target is None:
                findings.append(Finding(
                    0, "DEP-LINT-STATUS-CONTAMINATION", "dep/claims.yaml", 0,
                    f"{node.get('id')}: dependency {dep!r} is not ledgered"))
                continue
            if str(target.get("completeness")) != "complete" or \
                    str(target.get("claim_status")) not in ok_statuses:
                findings.append(Finding(
                    0, "DEP-LINT-STATUS-CONTAMINATION", "dep/claims.yaml", 0,
                    f"{node.get('id')} (complete) depends on {dep!r} with "
                    f"status {target.get('claim_status')}/{target.get('completeness')}"))


def rule_block(cfg, claims, findings: list[Finding]) -> None:
    """DEP-LINT-BLOCK (Sev 1): required fields on every ledger node."""
    for node in claims["results"]:
        for field in cfg["required_result_fields"]:
            if field not in node:
                findings.append(Finding(
                    1, "DEP-LINT-BLOCK", "dep/claims.yaml", 0,
                    f"{node.get('id')}: result missing required field {field!r}"))
    for section in ("conjectures", "empirical"):
        for node in claims[section]:
            for field in cfg["required_claim_fields"]:
                if field not in node:
                    findings.append(Finding(
                        1, "DEP-LINT-BLOCK", "dep/claims.yaml", 0,
                        f"{node.get('id')}: missing required field {field!r}"))


def rule_hyp_declared(cfg, claims, findings: list[Finding]) -> None:
    """DEP-LINT-HYP-DECLARED (Sev 0): hypotheses of results are ledgered in
    dep/hypotheses.yaml."""
    path = REPO / "dep" / "hypotheses.yaml"
    ledgered: dict[str, set[str]] = {}
    if path.exists():
        for entry in load_yaml_list(path):
            node = str(entry.get("node", ""))
            ledgered.setdefault(node, set()).add(str(entry.get("hyp", "")))
    for node in claims["results"]:
        for hyp in node.get("hyp", []) or []:
            if str(hyp) not in ledgered.get(str(node.get("id")), set()):
                findings.append(Finding(
                    0, "DEP-LINT-HYP-DECLARED", "dep/claims.yaml", 0,
                    f"{node.get('id')}: hypothesis {hyp!r} not found in dep/hypotheses.yaml"))


def rule_fidelity(cfg, claims, findings: list[Finding]) -> None:
    """DEP-LINT-FIDELITY (Sev 0): machine-checked results carry fidelity files."""
    for node in claims["results"]:
        if str(node.get("claim_status")) != "machine-checked":
            continue
        fidelity = str(node.get("fidelity", ""))
        if not fidelity or not (REPO / fidelity).exists():
            findings.append(Finding(
                0, "DEP-LINT-FIDELITY", "dep/claims.yaml", 0,
                f"{node.get('id')}: machine-checked result lacks a fidelity mapping ({fidelity!r})"))


def rule_degeneracy(cfg, claims, findings: list[Finding]) -> None:
    """DEP-LINT-DEGENERACY (Sev 1): degeneracy artifacts exist and meet quota."""
    for node in claims["results"]:
        ref = str(node.get("degeneracy", ""))
        if not ref or not (REPO / ref).exists():
            findings.append(Finding(
                1, "DEP-LINT-DEGENERACY", "dep/claims.yaml", 0,
                f"{node.get('id')}: degeneracy artifact missing ({ref!r})"))
            continue
        data = json.loads((REPO / ref).read_text())
        if not data.get("summary", {}).get("quota_met", False):
            findings.append(Finding(
                1, "DEP-LINT-DEGENERACY", ref, 0,
                f"{node.get('id')}: degeneracy quota not met"))


def rule_axiom_drift(cfg, claims, findings: list[Finding]) -> None:
    """DEP-LINT-AXIOM-DRIFT (Sev 0): extracted axioms equal the declared ledger."""
    declared = {}
    path = REPO / "dep" / "axioms.yaml"
    if path.exists():
        for entry in load_yaml_list(path):
            if str(entry.get("node", "")).startswith("IGTP."):
                declared[entry["node"]] = set(entry.get("axioms", []))
    extracted_path = REPO / "dep" / "out" / "axioms.json"
    if not extracted_path.exists():
        findings.append(Finding(
            0, "DEP-LINT-AXIOM-DRIFT", "dep/out/axioms.json", 0,
            "extracted axiom ledger missing; run tools/axioms/extract_axioms.py"))
        return
    extracted = json.loads(extracted_path.read_text())["results"]
    for node, axioms in sorted(extracted.items()):
        if node in declared and set(axioms) != declared[node]:
            findings.append(Finding(
                0, "DEP-LINT-AXIOM-DRIFT", "dep/axioms.yaml", 0,
                f"{node}: declared {sorted(declared[node])} != extracted {sorted(axioms)}"))
    for node in sorted(declared):
        if node not in extracted:
            findings.append(Finding(
                0, "DEP-LINT-AXIOM-DRIFT", "dep/axioms.yaml", 0,
                f"{node}: declared in the ledger but absent from the extraction"))


def rule_gap_expiry(cfg, findings: list[Finding]) -> None:
    """DEP-LINT-GAP-EXPIRY (Sev 1): expired gaps fail the build."""
    path = REPO / "dep" / "gaps.yaml"
    if not path.exists():
        return
    for entry in load_yaml_list(path):
        expires = str(entry.get("expires", ""))
        if expires and re.match(r"^\d{4}-\d{2}-\d{2}$", expires):
            today = _declared_today(cfg)
            if expires < today:
                findings.append(Finding(
                    1, "DEP-LINT-GAP-EXPIRY", "dep/gaps.yaml", 0,
                    f"gap {entry.get('id', '?')} expired on {expires}"))


def _declared_today(cfg) -> str:
    """Build date declared in the configuration, never the system clock
    (deterministic builds; Chapter 6.2)."""
    return str(cfg.get("build_date", "2026-11-07"))


def rule_doc_sync(cfg, findings: list[Finding]) -> None:
    """DEP-LINT-DOC-SYNC (Sev 1): configured rules equal the implemented catalog."""
    configured = list(cfg.get("rules", []))
    if sorted(configured) != sorted(RULE_CATALOG):
        findings.append(Finding(
            1, "DEP-LINT-DOC-SYNC", ".dep/dep_lint.json", 0,
            f"configuration rules {sorted(set(configured) ^ set(RULE_CATALOG))} "
            "differ from the implemented catalog"))


LEAN_DECLARATIONS = re.compile(
    r"^\s*(?:noncomputable\s+)?(?:private\s+)?"
    r"(theorem|def|class|structure|instance|abbrev)\s+([\w'.]+)"
)


def rule_docstrings(cfg, findings: list[Finding]) -> None:
    """DEP-LINT-DOCSTRINGS (Sev 2): public Lean declarations carry docstrings."""
    for base in cfg["lean_scan"]:
        root = REPO / base
        for path in iter_files(root, [".lean"], cfg["exempt_paths"]):
            rel = path.relative_to(REPO).as_posix()
            text = path.read_text()
            lines = text.splitlines()
            doc_opens, _ = lean_docstring_lines(text)
            # line index of the opening line for each comment block end
            block_end_to_open: dict[int, int] = {}
            i = 0
            while i < len(lines):
                if lines[i].lstrip().startswith("/-"):
                    start = i
                    while i < len(lines) and "-/" not in lines[i]:
                        i += 1
                    block_end_to_open[i] = start
                i += 1
            for lineno, line in enumerate(lines):
                m = LEAN_DECLARATIONS.match(line)
                if not m:
                    continue
                if m.group(1) == "instance" or m.group(2).startswith("_"):
                    continue
                prev = lineno - 1
                if prev in block_end_to_open and \
                        block_end_to_open[prev] in doc_opens:
                    continue
                findings.append(Finding(
                    2, "DEP-LINT-DOCSTRINGS", rel, lineno + 1,
                    f"declaration {m.group(2)!r} lacks a /-- docstring"))


def generate_results_table(claims: dict) -> str:
    """Regenerate dep/out/results_table.md from the claims ledger."""
    header = (
        "# Results table (generated; never hand-edited)\n\n"
        "| ID | Node | Statement | Claim status | Complete? | Depends on | Witness | Gap |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )
    rows = []
    for node in claims["results"] + claims["conjectures"] + claims["empirical"]:
        statement = str(node.get("statement", "")).replace("|", "\\|")
        if len(statement) > 160:
            statement = statement[:157] + "..."
        rows.append(
            f"| {node.get('id')} | {node.get('node', '-')} | {statement} "
            f"| {node.get('claim_status')} | {node.get('completeness')} "
            f"| {', '.join(node.get('depends', []) or []) or '-'} "
            f"| {str(node.get('witness', '-')).replace('|', '\\|')} "
            f"| {node.get('gap', '-')} |"
        )
    return header + "\n".join(rows) + "\n"


def rule_results_table(cfg, claims, findings: list[Finding], update: bool) -> None:
    """DEP-LINT-RESULTS-TABLE (Sev 1): the committed table matches regeneration."""
    table = generate_results_table(claims)
    out = REPO / "dep" / "out" / "results_table.md"
    if update:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(table)
        return
    if not out.exists():
        findings.append(Finding(
            1, "DEP-LINT-RESULTS-TABLE", "dep/out/results_table.md", 0,
            "generated results table missing; run dep_lint --update-results"))
        return
    if out.read_text() != table:
        findings.append(Finding(
            1, "DEP-LINT-RESULTS-TABLE", "dep/out/results_table.md", 0,
            "generated results table is stale; run dep_lint --update-results"))


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def run_lint(cfg: dict) -> list[Finding]:
    findings: list[Finding] = []
    rule_admitted(cfg, findings)
    rule_banned_phrase(cfg, findings)
    claims = _load_claims(findings)
    rule_status_value(cfg, claims, findings)
    rule_status_contamination(cfg, claims, findings)
    rule_block(cfg, claims, findings)
    rule_hyp_declared(cfg, claims, findings)
    rule_fidelity(cfg, claims, findings)
    rule_degeneracy(cfg, claims, findings)
    rule_axiom_drift(cfg, claims, findings)
    rule_gap_expiry(cfg, findings)
    rule_doc_sync(cfg, findings)
    rule_docstrings(cfg, findings)
    rule_results_table(cfg, claims, findings, update=False)
    findings.sort(key=lambda f: f.key())
    return findings


def self_test(cfg: dict) -> int:
    """--self-test: fixtures must produce the exact expected finding counts."""
    fixtures = REPO / "tools" / "dep_lint" / "fixtures"
    expected_path = fixtures / "expected.json"
    if not expected_path.exists():
        print("self-test: fixtures/expected.json missing", file=sys.stderr)
        return 1
    expected = json.loads(expected_path.read_text())
    by_rule: dict[str, int] = {}

    # Banned phrases: the fixture document.
    doc = fixtures / "bad_doc.md"
    count = 0
    low = doc.read_text().lower()
    for phrase in cfg["banned_phrases"]:
        if phrase in set(cfg["banned_phrase_word_boundaries"]):
            count += len(re.findall(rf"\b{re.escape(phrase)}\b", low))
        else:
            count += low.count(phrase)
    by_rule["DEP-LINT-BANNED-PHRASE"] = count

    # Admitted tokens: the fixture Lean file.
    lean = (fixtures / "bad_lean.lean").read_text()
    admitted = sum(lean.count(tok) for tok in ["sorry", "admit", "native_decide"])
    by_rule["DEP-LINT-ADMITTED"] = admitted

    # Status values: the fixture claims file.
    bad_claims = load_yaml_list(fixtures / "bad_claims.yaml")
    bad_status = sum(1 for e in bad_claims
                     if e.get("claim_status") not in set(cfg["claim_status_vocabulary"]))
    by_rule["DEP-LINT-STATUS-VALUE"] = bad_status

    failures = []
    for rule, want in sorted(expected.items()):
        got = by_rule.get(rule)
        if got != want:
            failures.append(f"{rule}: expected {want} findings, counted {got}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("self-test: all scenarios match expected counts")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="DEP&CC 2.0 linter for IGTP")
    parser.add_argument("-c", "--config", default=str(CONFIG))
    parser.add_argument("-t", "--self-test", action="store_true")
    parser.add_argument("--update-results", action="store_true",
                        help="regenerate dep/out/results_table.md from the ledger")
    parser.add_argument("-v", "--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print("dep_lint 0.1.0 (DEP&CC 2.0)")
        return 0

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"bootstrap failure: configuration {config_path} missing", file=sys.stderr)
        return 2
    try:
        cfg = json.loads(config_path.read_text())
    except json.JSONDecodeError as exc:
        print(f"bootstrap failure: configuration parse error: {exc}", file=sys.stderr)
        return 2

    if args.self_test:
        return self_test(cfg)

    findings = run_lint(cfg)
    if args.update_results:
        claims = _load_claims(findings)
        rule_results_table(cfg, claims, [], update=True)
        print("results table regenerated")

    fail_on = set(cfg.get("fail_on", [0, 1]))
    failing = [f for f in findings if f.severity in fail_on]
    for f in findings:
        print(f.render())
    print(f"\ndep_lint: {len(findings)} findings, {len(failing)} failing "
          f"(fail_on={sorted(fail_on)})")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
