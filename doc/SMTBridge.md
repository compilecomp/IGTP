# SMTBridge

## Abstract

`igtp_engine.smt_bridge` wraps the pinned z3 solver behind an explicit
result-status policy with declared finite timeouts. It takes a z3 boolean
formula and a timeout in milliseconds; it produces an `SMTResult` whose
status is exactly one of `sat`, `unsat`, `unknown`.

## Formal Definitions

Python 3.12:

```python
class SMTStatus(Enum):
    SAT = "sat"
    UNSAT = "unsat"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class SMTResult:
    status: SMTStatus
    model: dict[str, bool] | None
    solver_version: str
    wall_seconds: float | None   # informational; never load-bearing

def check(formula: z3.BoolRef, timeout_ms: int = 10000) -> SMTResult
def propositional(assignments: dict[str, bool],
                  clauses: list[frozenset[str]]) -> z3.BoolRef
```

Pinned dependency: `z3-solver==4.13.0.0` (requirements.txt;
`dep/toolchain.lock`); `solver_version()` returns the running interpreter's
version and artifacts record it.

## Algorithm

`check` validates the timeout (policy P1: a positive integer is required;
violations raise `ValueError`), configures z3 with `timeout` set to the
declared value, runs the check, and maps the raw verdict through
`_interpret`: `z3.sat` to SAT (with a completed model), `z3.unsat` to UNSAT,
everything else to UNKNOWN (policy P2: `unknown` and timeout are never
reported as success). Wall-clock time is measured for the informational
record only and is excluded from golden comparisons (arithmetic class
`heuristic-numeric`, DEP&CC 2.0 Chapter 18.1). Complexity: delegated to z3;
no re-encoding beyond clause construction in `propositional`.

## Invariants

1. P1: every invocation carries a finite, declared timeout; the bridge
   refuses to run without one.
2. P2: `_interpret` maps `z3.unknown` to `SMTStatus.UNKNOWN`; no code path
   treats `unknown` or timeout as `unsat` (test `test_unknown_stays_unknown`).
3. P4: no claim in `dep/claims.yaml` rests on a z3 verdict alone; z3 is an
   independent cross-check of the resolution engine and is listed in the
   trusted-computing base with that restriction (`dep/axioms.yaml`, `tcb`).

## Integration Points

Depends on: z3 4.13.0 (pinned), Python 3.12. Depended on by: the demo
pipeline (stage 4), the test suite (`test_smt_bridge.py`). Cross-language:
the resolution engine produces the entailment decisions; z3 verifies them
independently, and the two engines must agree on the pipeline tasks
(`emp.smt_crosscheck`).

## Known Limitations

The bridge handles Boolean formulas and zero-arity model declarations only;
no uninterpreted functions, arrays, or arithmetic theories are exposed by
this interface. `unknown` results carry no diagnosis. The timeout is
advisory inside z3 in rare internal cases; a verdict arriving after the
declared budget is still classified honestly, but the wall time may exceed
the budget, and the wall time is informational. Nonlinear or quantified
inputs may return `unknown`; the policy records that outcome instead of
guessing.
