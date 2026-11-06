"""SMT bridge: z3 with declared finite timeouts and explicit result status.

Policy (DEP&CC 2.0, Chapter 19.8):
  P1. Every invocation declares a finite timeout in milliseconds.
  P2. `unknown` and timeout are distinct from `unsat` and are never reported
      as success. `SMTStatus.UNKNOWN` is the only honest representation.
  P3. The solver version is pinned (requirements.txt: z3-solver==4.13.0.0) and
      recorded in every result artifact.
  P4. `unsat` from z3 is a trusted-computing-base entry (dep/axioms.yaml,
      tcb.z3): the reference engine uses z3 as an independent cross-check of
      the resolution engine, never as the sole justification of a claim.

Wall-clock time is recorded as informational output only; it is excluded from
golden comparisons and never load-bearing (arithmetic class of timings:
`heuristic-numeric`, Chapter 18.1).
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum

import z3

PinnedVersion = "4.13.0"


class SMTStatus(Enum):
    SAT = "sat"
    UNSAT = "unsat"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SMTResult:
    status: SMTStatus
    model: dict[str, bool] | None
    solver_version: str
    wall_seconds: float | None  # informational; never load-bearing


def _interpret(check_result: z3.CheckSatResult, model: z3.ModelRef | None) -> SMTStatus:
    """Map a raw z3 result to the explicit status. UNKNOWN stays UNKNOWN."""
    if check_result == z3.sat:
        return SMTStatus.SAT
    if check_result == z3.unsat:
        return SMTStatus.UNSAT
    return SMTStatus.UNKNOWN


def solver_version() -> str:
    """The pinned z3 version string of the running interpreter."""
    return z3.get_version_string()


def check(formula: z3.BoolRef, timeout_ms: int = 10000) -> SMTResult:
    """Check satisfiability with a declared finite timeout.

    Raises ValueError if timeout_ms is not a positive integer (policy P1).
    """
    if not isinstance(timeout_ms, int) or timeout_ms <= 0:
        raise ValueError("timeout_ms must be a positive integer (declared timeout)")
    solver = z3.Solver()
    solver.set("timeout", timeout_ms)
    solver.add(formula)
    start = time.perf_counter()
    raw = solver.check()
    model = None
    if raw == z3.sat:
        z3_model = solver.model()
        model = {
            d.name(): bool(z3.is_true(z3_model.eval(d(), model_completion=True)))
            for d in z3_model.decls()
            if d.arity() == 0
        }
    wall = time.perf_counter() - start
    return SMTResult(
        status=_interpret(raw, model),
        model=model,
        solver_version=solver_version(),
        wall_seconds=wall,
    )


def propositional(assignments: dict[str, bool], clauses: list[frozenset[str]]) -> z3.BoolRef:
    """Build a z3 formula equivalent to the conjunction of the given clauses.

    Clauses use the literal tags of the resolution engine: '+x' and '-x'.
    """
    exprs = []
    for clause in clauses:
        lits = []
        for lit in sorted(clause):
            b = z3.Bool(lit[1:])
            lits.append(b if lit.startswith("+") else z3.Not(b))
        exprs.append(z3.Or(*lits) if lits else z3.BoolVal(False))
    return z3.And(*exprs) if exprs else z3.BoolVal(True)
