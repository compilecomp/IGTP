"""Propositional resolution engine: the ATP component of the reference engine.

The engine refutes the negation of a goal formula under premise clauses by
saturating the clause set under binary resolution with subsumption pruning.
For propositional logic, saturation decides satisfiability: the procedure is
sound and refutation-complete.

Claim status (dep/claims.yaml, res.engine): `empirical`. Soundness of every
produced derivation is machine-checked against a clause-level criterion by
`check_derivation`, and the test suite exercises both outcomes; no formal
verification of the engine itself is claimed.

Complexity: the clause set over n variables has at most 3^n clauses, so
saturation terminates; the worst-case cost is O(9^n) pair inspections. This
exponential bound is a property of resolution, not of an implementation
optimization, and is declared here rather than hidden.

Justification discipline (DEP&CC 2.0, Chapter 19.8, applied to the SMT/ATP
boundary): this engine never reports `unknown`; it either derives the empty
clause (goal refuted) or saturates without it (goal not entailed by
resolution within the declared bound).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction  # noqa: F401  (kept for uniform exact-arithmetic policy)

# ---------------------------------------------------------------------------
# Formulas
# ---------------------------------------------------------------------------


def var(name: str) -> tuple:
    return ("var", name)


def neg(f: tuple) -> tuple:
    return ("not", f)


def conj(a: tuple, b: tuple) -> tuple:
    return ("and", a, b)


def disj(a: tuple, b: tuple) -> tuple:
    return ("or", a, b)


def implies(a: tuple, b: tuple) -> tuple:
    return ("implies", a, b)


def variables(f: tuple) -> set[str]:
    kind = f[0]
    if kind == "var":
        return {f[1]}
    if kind == "not":
        return variables(f[1])
    return variables(f[1]) | variables(f[2])


# ---------------------------------------------------------------------------
# CNF conversion
# ---------------------------------------------------------------------------


def _literal(f: tuple) -> frozenset[str]:
    """Literal of an NNF atom; returns the signed literal tag."""
    if f[0] == "var":
        return frozenset({f"+{f[1]}"})
    if f[0] == "not" and f[1][0] == "var":
        return frozenset({f"-{f[1][1]}"})
    raise ValueError(f"not a literal in NNF: {f}")


def _nnf(f: tuple, polarity: bool) -> tuple:
    """Negation normal form under the given polarity.

    Positive polarity preserves the connective; negative polarity applies the
    De Morgan dual: the negation of a conjunction is a disjunction of
    negations, and the negation of a disjunction is a conjunction of
    negations.
    """
    kind = f[0]
    if kind == "var":
        return f if polarity else neg(f)
    if kind == "not":
        return _nnf(f[1], not polarity)
    if kind == "implies":
        return _nnf(disj(neg(f[1]), f[2]), polarity)
    if kind == "and":
        if polarity:
            return conj(_nnf(f[1], True), _nnf(f[2], True))
        return disj(_nnf(f[1], False), _nnf(f[2], False))
    if kind == "or":
        if polarity:
            return disj(_nnf(f[1], True), _nnf(f[2], True))
        return conj(_nnf(f[1], False), _nnf(f[2], False))
    raise ValueError(f"unknown connective: {kind}")


def _distribute(f: tuple) -> list[frozenset[str]]:
    """CNF of an NNF formula as a list of clauses (a conjunction of disjunctions)."""
    kind = f[0]
    if kind == "and":
        return _distribute(f[1]) + _distribute(f[2])
    if kind == "or":
        out = []
        for c1 in _distribute(f[1]):
            for c2 in _distribute(f[2]):
                out.append(c1 | c2)
        return out
    return [_literal(f)]


def cnf(f: tuple) -> list[frozenset[str]]:
    """Clausal normal form of a propositional formula, deduplicated and sorted.

    Deterministic: the output list is sorted by the sorted literal tags of
    each clause; the order is a function of the formula alone.
    """
    clauses = set(_distribute(_nnf(f, True)))
    return sorted(clauses, key=lambda c: sorted(c))


def negate(f: tuple) -> tuple:
    return neg(f)


# ---------------------------------------------------------------------------
# Resolution saturation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResolutionStep:
    """One derived clause with its justification.

    rule is "input" for premises and "resolution" for derived clauses; for
    resolution steps, `parents` holds the two parent clause indices in the
    derivation list and `on_literal` the complementary pair eliminated.
    """

    clause: frozenset[str]
    rule: str
    parents: tuple[int, int] | None
    on_literal: str | None


@dataclass(frozen=True)
class ResolutionOutcome:
    refuted: bool
    derivation: list[ResolutionStep]
    clause_count: int


def _complement(lit: str) -> str:
    return ("-" if lit.startswith("+") else "+") + lit[1:]


def _resolve(c1: frozenset[str], c2: frozenset[str], lit: str) -> frozenset[str]:
    return (c1 - {lit}) | (c2 - {_complement(lit)})


def _subsumed(clause: frozenset[str], clauses: list[frozenset[str]]) -> bool:
    return any(other <= clause for other in clauses if other != clause)


def saturate(
    premises: list[frozenset[str]], max_clauses: int | None = None
) -> ResolutionOutcome:
    """Saturate the premise set under binary resolution.

    Returns refuted=True iff the empty clause is derived. Raises RuntimeError
    if the clause set would exceed max_clauses (default 3^n over the variables
    occurring in the premises), which is the declared termination bound.
    """
    nvars = len({lit[1:] for clause in premises for lit in clause})
    bound = max_clauses if max_clauses is not None else 3 ** max(nvars, 1)

    derivation: list[ResolutionStep] = [
        ResolutionStep(clause, "input", None, None) for clause in premises
    ]
    clause_set: list[frozenset[str]] = list(premises)
    seen: set[frozenset[str]] = set(premises)

    if any(len(c) == 0 for c in clause_set):
        return ResolutionOutcome(True, derivation, len(clause_set))

    i = 0
    while i < len(clause_set):
        c1 = clause_set[i]
        j = i + 1
        while j < len(clause_set):
            c2 = clause_set[j]
            for lit in sorted(c1):
                comp = _complement(lit)
                if comp in c2:
                    resolvent = _resolve(c1, c2, lit)
                    if len(resolvent) == 0:
                        derivation.append(
                            ResolutionStep(frozenset(), "resolution", (i, j), lit)
                        )
                        return ResolutionOutcome(True, derivation, len(clause_set) + 1)
                    if resolvent not in seen and not _subsumed(resolvent, clause_set):
                        if len(clause_set) + 1 > bound:
                            raise RuntimeError(
                                f"clause bound {bound} exceeded; declared "
                                "termination bound of propositional resolution"
                            )
                        clause_set.append(resolvent)
                        seen.add(resolvent)
                        derivation.append(
                            ResolutionStep(resolvent, "resolution", (i, j), lit)
                        )
            j += 1
        i += 1
    return ResolutionOutcome(False, derivation, len(clause_set))


def check_derivation(
    premises: list[frozenset[str]], derivation: list[ResolutionStep]
) -> bool:
    """Verify a derivation against the clause-level soundness criterion.

    Every input step must be a premise. Every resolution step with parents
    p, q and eliminated literal L must have its clause a subset of
    (C_p ∪ C_q) \\ {L, ~L}. Returns True iff every step passes.
    """
    premise_set = {c for c in premises}
    clauses_by_index: list[frozenset[str]] = []
    for step in derivation:
        if step.rule == "input":
            if step.clause not in premise_set:
                return False
        elif step.rule == "resolution":
            if step.parents is None:
                return False
            p, q = step.parents
            if p >= len(clauses_by_index) or q >= len(clauses_by_index):
                return False
            union = clauses_by_index[p] | clauses_by_index[q]
            if step.on_literal is None or step.clause - union:
                return False
            removed = {step.on_literal, _complement(step.on_literal)}
            if (union - step.clause) & removed != removed:
                return False
        else:
            return False
        clauses_by_index.append(step.clause)
    return True


def tautology(formula: tuple) -> ResolutionOutcome:
    """Decide whether `formula` is a tautology by refuting its negation."""
    clauses = cnf(negate(formula))
    return saturate(clauses)
