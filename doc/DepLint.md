# DepLint

## Abstract

`tools/dep_lint/dep_lint.py` is the mechanical enforcement layer of DEP&CC 2.0
for this repository. It takes the configuration `.dep/dep_lint.json` and the
repository tree; it produces findings sorted by (file, line, rule, message)
and an exit code. It is a DEP-2 tool subject to the standard: it is lexical
and structural, it does not decide mathematical truth, and kernel checking
happens in Lean.

## Formal Definitions

Python 3.12 command line:

```text
dep_lint [options]
  -c, --config <path>     default .dep/dep_lint.json
  -t, --self-test         run the fixture scenarios, compare exact counts
  --update-results        regenerate dep/out/results_table.md from the ledger
  -v, --version
```

Exit codes (Chapter 33.1): 0 no failing findings; 1 failing findings at a
severity in `fail_on`, or failed self-test; 2 bootstrap failure; 3 usage
error.

Implemented rules (the catalog must equal the `rules` array of the
configuration; `DEP-LINT-DOC-SYNC` enforces this):

| Rule | Severity | Chapter |
|---|---|---|
| DEP-LINT-ADMITTED | 0 | 19.1 |
| DEP-LINT-BANNED-PHRASE | 1 | 22.1, Appendix A |
| DEP-LINT-STATUS-VALUE | 1 | 5.4, 5.5 |
| DEP-LINT-STATUS-CONTAMINATION | 0 | 5.5 |
| DEP-LINT-BLOCK | 1 | 32.2 |
| DEP-LINT-HYP-DECLARED | 0 | Law 1, 9.2 |
| DEP-LINT-FIDELITY | 0 | 19.5 |
| DEP-LINT-DEGENERACY | 1 | 30.3 |
| DEP-LINT-AXIOM-DRIFT | 0 | 19.2 |
| DEP-LINT-GAP-EXPIRY | 1 | 23.6 |
| DEP-LINT-DOC-SYNC | 1 | 33 |
| DEP-LINT-DOCSTRINGS | 2 | doc standard 5 |
| DEP-LINT-RESULTS-TABLE | 1 | 23.3 |

## Algorithm

The scan order is fixed: Lean sources (comment-stripped) for banned tokens;
documents for banned phrases (word-boundary matching for the phrases so
marked); the claims ledger for status vocabulary, contamination along
`depends`, required fields, hypothesis coverage, fidelity and degeneracy
artifacts; the extracted axiom dump against the declared ledger; the gap
register against the declared build date; the Lean docstring linter; and the
results-table regeneration. All patterns, thresholds, vocabularies, and the
build date live in `.dep/dep_lint.json`. Time complexity is linear in the
scanned input size. Determinism: sorted traversal, sorted findings, a
declared build date instead of the system clock, no network access.

## Invariants

1. The rule catalog in code equals the `rules` array in the configuration.
2. Findings are total-ordered by (file, line, rule, message); two runs on
   the same tree produce identical output.
3. `--self-test` compares fixture scenarios against exact expected counts
   (`tools/dep_lint/fixtures/expected.json`).

## Integration Points

Depends on: Python 3.12 standard library (`json`, `re`, `argparse`,
`pathlib`). Depended on by: the CI lint job, the developer workflow. The
generated results table `dep/out/results_table.md` is consumed by
`README.md` and by review.

## Known Limitations

The linter is lexical: it checks coverage of fields and vocabularies, not
truthfulness of their content (Chapter 33.4). Fidelity mappings are checked
for existence, not honesty. The YAML reader handles the flat ledger schemas
of this repository only; nested YAML outside the documented schemas is not
parsed. Claiming that a passing lint run implies a correct repository is a
violation of the standard, not a property of the tool.
