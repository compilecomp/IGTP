# LeanBridge

## Abstract

`igtp_engine.lean_bridge` emits Lean 4 certificate files for proof tasks
decided by the reference engine. It takes a list of `LeanTask` records; it
produces a deterministic Lean source file that the pinned toolchain
kernel-checks in CI.

## Formal Definitions

Python 3.12:

```python
@dataclass(frozen=True)
class LeanTask:
    name: str               # ASCII identifier
    prop_vars: list[str]    # propositional variables, declaration order
    hypotheses: list[str]   # Lean formulas as hypothesis types
    conclusion: str         # Lean formula as the conclusion type

def emit_lean_certificate(tasks: list[LeanTask]) -> str
```

Emitted file format: a generated-header comment block (marked DO NOT EDIT),
`import IGTP`, then one declaration per task in sorted name order:

```lean
theorem igtp_demo_logic_1 {P : Prop} {Q : Prop} {R : Prop}
    (h1 : (P → Q)) (h2 : (Q → R)) (h3 : P) : R := by
  tauto
```

## Algorithm

Deterministic emission: tasks are sorted by name; hypothesis binders are
generated as h1..hk in list order; each declaration ends in `by tauto`, so
the Lean kernel re-proves the statement from the hypotheses. The emitted
bytes are a function of the task list alone (test
`test_output_is_deterministic`, including input-order invariance). The demo
records the SHA-256 of the certificate in `experiments/results/` and CI runs
`lake env lean` on the emitted file, so the artifact is rejected the moment
it stops compiling under the pinned toolchain.

## Invariants

1. The output contains no `sorry`, `admit`, or `native_decide`; the emitted
   tactic is `tauto` on explicit hypotheses.
2. Emission is deterministic and input-order invariant.
3. The certificate is a generated artifact under `dep/out/`; it is never
   hand-edited, and its content hash is recorded by the demo runner.

## Integration Points

Depends on: the IGTP Lean package (the emitted file imports IGTP; `tauto`
comes from Mathlib through that import). Depended on by: the demo pipeline
(stage 5) and the CI Lean job, which kernel-checks the artifact. This module
realizes Goal 3 of `doc/DesignGoals.md` at the artifact level: the human-
readable record of a task is emitted for independent verification by the
proof assistant.

## Known Limitations

Scope: propositional logic through `tauto`; no arithmetic, quantifiers, or
custom inductive types. The bridge transfers tasks; Lean re-proves them, so
the Python engine's derivation confers no verification guarantee
(DEP&CC 2.0 Chapter 19.6: no refinement claim is made from the Python engine
to the Lean artifact, and none may be claimed). Emission fails on
non-ASCII or colliding task names by contract of `LeanTask.name`; validation
beyond that is the caller's duty.
