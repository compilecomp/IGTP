"""Tests for the propositional resolution engine.

Covers: CNF conversion, refutation and satisfaction outcomes, derivation
soundness against the clause-level criterion, and the declared termination
bound.
"""

import pytest

from igtp_engine import resolution as R


def A() -> tuple:
    return R.var("A")


def B() -> tuple:
    return R.var("B")


def C() -> tuple:
    return R.var("C")


def test_cnf_of_implication() -> None:
    clauses = R.cnf(R.implies(A(), B()))
    assert clauses == [frozenset({"-A", "+B"})]


def test_cnf_distributes() -> None:
    formula = R.disj(R.conj(A(), B()), C())
    clauses = R.cnf(formula)
    assert [set(c) for c in clauses] == [{"+A", "+C"}, {"+B", "+C"}]


def test_cnf_deterministic_ordering() -> None:
    formula = R.conj(R.disj(A(), B()), R.disj(B(), C()))
    assert R.cnf(formula) == R.cnf(formula)
    assert R.cnf(formula) == sorted(R.cnf(formula), key=lambda c: sorted(c))


def test_tautology_refuted() -> None:
    outcome = R.tautology(R.disj(A(), R.neg(A())))
    assert outcome.refuted
    assert R.check_derivation(R.cnf(R.negate(R.disj(A(), R.neg(A())))), outcome.derivation)


def test_modus_ponens_entailment() -> None:
    hyps = [R.implies(A(), B()), A()]
    goal = B()
    premise_clauses = [c for h in hyps for c in R.cnf(h)]
    outcome = R.saturate(premise_clauses + R.cnf(R.negate(goal)))
    assert outcome.refuted
    assert R.check_derivation(premise_clauses + R.cnf(R.negate(goal)), outcome.derivation)


def test_non_entailment_saturates() -> None:
    hyps = [R.implies(A(), B())]
    goal = A()  # not entailed
    premise_clauses = [c for h in hyps for c in R.cnf(h)]
    outcome = R.saturate(premise_clauses + R.cnf(R.negate(goal)))
    assert not outcome.refuted


def test_derivation_soundness_detects_tampering() -> None:
    """A tampered derivation must fail the clause-level criterion."""
    premises = [frozenset({"+A"}), frozenset({"-A"})]
    outcome = R.saturate(premises)
    assert outcome.refuted
    assert R.check_derivation(premises, outcome.derivation)
    tampered = list(outcome.derivation)
    tampered[-1] = R.ResolutionStep(frozenset({"+A"}), "resolution", (0, 1), "+A")
    assert not R.check_derivation(premises, tampered)


def test_clause_bound_raises() -> None:
    premises = [frozenset({"+A", "+B"}), frozenset({"-A", "-B"})]
    with pytest.raises(RuntimeError):
        R.saturate(premises, max_clauses=2)


def test_saturate_is_deterministic() -> None:
    premises = R.cnf(R.implies(R.implies(A(), B()), R.implies(R.implies(B(), C()), R.implies(A(), C()))))
    first = R.saturate(premises + R.cnf(R.negate(R.implies(A(), C()))))
    second = R.saturate(premises + R.cnf(R.negate(R.implies(A(), C()))))
    assert first.refuted == second.refuted
    assert first.clause_count == second.clause_count
    assert [s.clause for s in first.derivation] == [s.clause for s in second.derivation]


def test_empty_clause_input_refutes_immediately() -> None:
    outcome = R.saturate([frozenset()])
    assert outcome.refuted
