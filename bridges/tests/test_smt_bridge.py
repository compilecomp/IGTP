"""Tests for the SMT bridge: timeout policy, status honesty, cross-checks.

Policy under test (doc/SMTBridge.md):
  P1  finite declared timeouts, enforced by validation;
  P2  UNKNOWN is never mapped to UNSAT or SAT;
  P4  z3 verdicts agree with the resolution engine on propositional tasks.
"""

import pytest
import z3

from igtp_engine import resolution as R
from igtp_engine import smt_bridge
from igtp_engine.smt_bridge import SMTStatus, _interpret


def test_timeout_must_be_positive() -> None:
    with pytest.raises(ValueError):
        smt_bridge.check(z3.Bool("x"), timeout_ms=0)
    with pytest.raises(ValueError):
        smt_bridge.check(z3.Bool("x"), timeout_ms=-5)


def test_unknown_stays_unknown() -> None:
    """The interpretation of a raw z3 `unknown` is UNKNOWN, never UNSAT (P2)."""
    assert _interpret(z3.unknown, None) is SMTStatus.UNKNOWN
    assert _interpret(z3.sat, None) is SMTStatus.SAT
    assert _interpret(z3.unsat, None) is SMTStatus.UNSAT


def test_sat_and_unsat_on_propositional_input() -> None:
    x, y = z3.Bools("x y")
    sat = smt_bridge.check(z3.Or(x, y), timeout_ms=10000)
    assert sat.status is SMTStatus.SAT
    assert sat.model is not None
    unsat = smt_bridge.check(z3.And(x, z3.Not(x)), timeout_ms=10000)
    assert unsat.status is SMTStatus.UNSAT
    assert unsat.model is None


def test_solver_version_is_pinned() -> None:
    assert smt_bridge.solver_version() == smt_bridge.PinnedVersion


def test_z3_agrees_with_resolution_on_tasks() -> None:
    """Cross-engine agreement (P4) on the propositional entailments."""
    P, Q = R.var("P"), R.var("Q")
    cases = [
        ([R.implies(P, Q), P], Q, True),
        ([R.disj(P, Q), R.neg(P)], Q, True),
        ([R.implies(P, Q)], P, False),
    ]
    for hyps, goal, expected in cases:
        premise_clauses = [c for h in hyps for c in R.cnf(h)]
        outcome = R.saturate(premise_clauses + R.cnf(R.negate(goal)))
        assert outcome.refuted == expected
        premises = z3.And(*[smt_bridge_form(f) for f in hyps]) if hyps else z3.BoolVal(True)
        smt = smt_bridge.check(z3.Not(z3.Implies(premises, smt_bridge_form(goal))), timeout_ms=10000)
        assert (smt.status is SMTStatus.UNSAT) == expected


def smt_bridge_form(f: tuple):
    from igtp_engine.pipeline import z3_formula

    return z3_formula(f)
