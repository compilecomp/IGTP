# IGTP — Information-Geometric Theorem Proving

IGTP is a theorem-proving framework that unifies SAT/SMT solving, automated
theorem proving, and interactive theorem proving on a shared state space with
a single objective. The state space is a manifold-like structure whose points
are mathematical concepts; proofs are paths on it; the objective combines
geodesic energy (ATP), a constraint potential (SMT), and a description-length
regularizer (ITP).

This repository implements the first conformance-checked slice of that
program under two repository standards: `standard.md` (DEP&CC 2.0:
Deduction-Exact Proofs and Clean Communication) and `doc standard.md`
(Documentation Style Guide). Both are normative; every file in this
repository is held to them.

## Scope and claim statuses

Claims are separated by status; the closed vocabularies are defined in
`standard.md`, Chapter 5, and the full mapping lives in `dep/claims.yaml`
with a generated summary in `dep/out/results_table.md`.

- The formal core (`IGTP.lean`, `IGTP/`) is machine-checked: eight theorems
  in five modules, every declaration proved, zero `sorry`/`admit`/
  `native_decide`, zero `axiom` declarations. The Lean kernel extracted the
  axiom ledger; every result depends only on the standard Mathlib axioms
  `propext`, `Classical.choice`, `Quot.sound` (`dep/out/axioms/`). CI
  re-extracts the ledger and fails on drift.
- The reference engine (`bridges/`) is empirical: a concept-graph manifold, a
  deterministic least-cost geodesic search, a propositional resolution engine,
  a pinned z3 bridge with declared finite timeouts, and a Lean certificate
  emitter. It is supported by 44 tests and a reproducible demo artifact
  (`experiments/results/demo_golden.json`); it is not machine-checked.
- The design targets of the program (polynomial search cost on the smoothed
  manifold, minimal-complexity proof selection, Ricci-flow pruning,
  curvature-guided conjecture generation) are conjectural. They are recorded
  with status `conjectural` in `dep/claims.yaml` and `doc/DesignGoals.md`;
  no complexity, minimality, or discovery claim is made anywhere in this
  repository.

The five design goals and their per-goal status are documented in
`doc/DesignGoals.md`.

## Standards adoption

- DEP&CC 2.0, profile `Core` (Appendix J), with a dated full-conformance plan
  in `dep/manifest.yaml`. Core covers: the fourteen laws, annotation and
  ledger requirements, the symbol registry and convention manifest,
  hypothesis discharge and acyclicity, the interchange ledger (currently
  empty: no interchange occurs in any load-bearing statement), zero claim
  inflation, zero admitted tokens, the banned-phrase list, and `dep_lint` at
  zero Severity 0/1 findings.
- The Documentation Style Guide governs every document in `doc/` (structure:
  Title, Abstract, Formal Definitions, Algorithm, Invariants, Integration
  Points, Known Limitations). Two adaptations are declared in
  `dep/manifest.yaml`: component signatures are given in Lean 4 and Python
  rather than Rust, and the CI documentation clause runs `lake build` plus
  `dep_lint` docstring enforcement rather than `cargo doc`.

## Repository layout

```text
IGTP.lean, IGTP/        Lean 4 formal core (pinned: leanprover/lean4:4.14.0,
                        Mathlib @ 4bbdccd9); all declarations proved
lakefile.lean           package definition with the pinned Mathlib revision
bridges/igtp_engine/    reference engine: manifold, objective, search,
                        resolution (ATP), smt_bridge (SMT), lean_bridge (ITP),
                        pipeline
bridges/tests/          pytest suite (44 tests, exact rational arithmetic)
doc/                    component documents (Documentation Style Guide)
dep/                    ledgers: toolchain.lock, manifest, conventions,
                        symbols, axioms, constants, interchanges, gaps,
                        claims, hypotheses, fidelity/
dep/out/                generated artifacts (axiom dumps, degeneracy battery,
                        results table, Lean certificate); never hand-edited
experiments/            demo experiment: code, golden artifact, run record
tools/axioms/           axiom-ledger extraction (Chapter 19.2)
tools/degeneracy/       degeneracy battery (Chapter 30.3)
tools/dep_lint/         mechanical enforcement (Chapter 33) + self-test
.github/workflows/      CI: Lean build + axiom extraction + certificate check,
                        Python tests + demo golden, dep_lint
standard.md             DEP&CC 2.0 (normative, unchanged)
doc standard.md         Documentation Style Guide (normative, unchanged)
```

## Build and verification

Prerequisites: `elan` (Lean version manager), Python 3.12, `pip`.

```bash
# Lean: pinned toolchain and Mathlib revision; downloads the mathlib cache
lake build

# Axiom ledger extraction (writes dep/out/axioms*)
python3 tools/axioms/extract_axioms.py

# Python engine: tests, demo, degeneracy battery
pip install -r requirements.txt
cd bridges && python3 -m pytest -q
cd ..
python3 experiments/code/run_demo.py          # compares against the golden artifact
python3 tools/degeneracy/run_battery.py       # Chapter 30.3 battery, exact arithmetic

# Mechanical enforcement (exit 1 on any Severity 0/1 finding)
python3 tools/dep_lint/dep_lint.py --self-test
python3 tools/dep_lint/dep_lint.py
```

CI runs all of the above on every push: the Lean job builds with the pinned
toolchain, extracts the axiom ledger, kernel-checks the generated
certificate; the Python job runs the tests and the demo golden comparison;
the lint job runs `dep_lint` and the degeneracy battery.

## Results

The full logical inventory is in `dep/out/results_table.md` (generated; two
pages or fewer by design). Summary:

- Eight machine-checked theorems: energy nonnegativity; discrete-action
  nonnegativity; the Ricci-flow characterization of time-constant families;
  one-step natural-gradient descent on the quadratic model (strict and
  non-strict); the update-definition transfer; anchor-set existence for
  consistent anchors; anchor invariance under path replacement.
- Each theorem carries: a statement-fidelity mapping (`dep/fidelity/`), a
  degeneracy battery record (`dep/out/degeneracy/`), per-hypothesis
  sharpness records (`dep/hypotheses.yaml`), non-vacuity witnesses in the
  Lean sources, and an extracted axiom set.
- Four empirical results for the engine: resolution soundness on the test
  battery, SMT cross-engine agreement, search optimality on the demo
  manifold, and pipeline determinism.
- Six conjectures (design targets) with status `conjectural`; the status
  contamination rule forbids complete results from depending on them.

## Limitations

The manifold interface is data-only: no topology, smoothness, bilinearity,
or metric-Ricci relation is enforced, so no differential-geometric theorem is
stated against it. The descent theorems cover the one-dimensional quadratic
model; the multidimensional case is `conj.multidim_descent`. The engine is
propositional; z3 is a cross-check, never a sole justification. The K
component is a nonnegative proxy; no statement about Kolmogorov complexity
is possible against it. Independent cold reads of the DEP-0 results are
scheduled in `dep/manifest.yaml` and have not yet been performed. The gap
register `dep/gaps.yaml` is empty: every claimed result is fully proved, and
every unproved target is recorded as a conjecture rather than a gap.

## License

Apache License 2.0 (`LICENSE`).
