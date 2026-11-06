#!/usr/bin/env python3
"""Extract the axiom ledger for every load-bearing result of the IGTP formal core.

Runs `lake env lean` on a generated `#print axioms` script, parses the kernel
output, and writes:
  dep/out/axioms/<result>.json   one file per result
  dep/out/axioms.json            merged ledger

Deterministic: results are processed in sorted order; output contains no
timestamps. Exit code 1 if any result fails to extract.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

RESULTS = [
    "IGTP.geodesicEnergy_nonneg",
    "IGTP.discreteAction_nonneg",
    "IGTP.isRicciFlow_const",
    "IGTP.quadratic_descent_strict",
    "IGTP.quadratic_descent_le",
    "IGTP.naturalGradientStep_descent_strict",
    "IGTP.exists_path_satisfies_anchors",
    "IGTP.satisfiesAnchor_congr",
]

REPO = Path(__file__).resolve().parents[2]


def main() -> int:
    lines = ["import IGTP"]
    for name in RESULTS:
        lines.append(f"#print axioms {name}")
    script = "\n".join(lines) + "\n"

    script_path = REPO / ".lake" / "axiom_dump.lean"
    script_path.write_text(script)
    try:
        proc = subprocess.run(
            ["lake", "env", "lean", str(script_path.relative_to(REPO))],
            cwd=REPO, capture_output=True, text=True, timeout=900,
        )
    finally:
        script_path.unlink(missing_ok=True)

    output = proc.stdout + proc.stderr
    ledger = {}
    missing = []
    pattern = re.compile(
        r"'([\w.]+)' depends on axioms: \[([^\]]*)\]|'([\w.]+)' does not depend on any axioms"
    )
    for match in pattern.finditer(output):
        if match.group(1):
            axioms = sorted(a.strip() for a in match.group(2).split(",") if a.strip())
            ledger[match.group(1)] = axioms
        else:
            ledger[match.group(3)] = []

    for name in RESULTS:
        if name not in ledger:
            missing.append(name)

    if missing:
        print("FAILED to extract axioms for:", *missing, sep="\n  ", file=sys.stderr)
        print("--- kernel output ---", file=sys.stderr)
        print(output, file=sys.stderr)
        return 1

    out_dir = REPO / "dep" / "out" / "axioms"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in RESULTS:
        (out_dir / f"{name}.json").write_text(json.dumps(
            {"result": name, "axioms": ledger[name]}, indent=2, sort_keys=True) + "\n")
    merged = REPO / "dep" / "out" / "axioms.json"
    merged.write_text(json.dumps(
        {"lean_toolchain": "leanprover/lean4:4.14.0",
         "mathlib_commit": "4bbdccd9c5f862bf90ff12f0a9e2c8be032b9a84",
         "results": {k: ledger[k] for k in sorted(ledger)}},
        indent=2, sort_keys=True) + "\n")
    for name in RESULTS:
        print(f"{name}: {ledger[name]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
