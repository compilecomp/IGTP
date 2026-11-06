# ResolutionEngine

## Abstract

`igtp_engine.resolution` is the ATP component of the reference engine: a
propositional resolution engine with subsumption pruning and recorded
derivations. It takes premises and a goal in a formula AST; it produces the
refutation decision, a derivation list, and a clause count.

## Formal Definitions

Python 3.12:

```python
def var(name: str) -> tuple                 # ('var', name)
def neg / conj / disj / implies(f, ...) -> tuple
def cnf(f: tuple) -> list[frozenset[str]]   # clauses over '+x' / '-x' tags
def negate(f: tuple) -> tuple
def saturate(premises: list[frozenset[str]],
             max_clauses: int | None = None) -> ResolutionOutcome
def check_derivation(premises, derivation) -> bool
def tautology(formula: tuple) -> ResolutionOutcome

@dataclass(frozen=True)
class ResolutionOutcome:
    refuted: bool
    derivation: list[ResolutionStep]
    clause_count: int

@dataclass(frozen=True)
class ResolutionStep:
    clause: frozenset[str]
    rule: str              # 'input' | 'resolution'
    parents: tuple[int, int] | None
    on_literal: str | None
```

## Algorithm

CNF conversion: implication elimination, polarity-based negation normal form
(De Morgan duals at negative polarity), distribution of disjunction over
conjunction; output deduplicated and sorted by literal tags. Saturation:
worklist saturation under binary resolution; for each complementary literal
pair across two clauses the resolvent is added unless subsumed or already
present; derivation steps record the parent indices and the eliminated
literal. Termination: the clause set over n variables has at most 3^n
elements; exceeding the declared bound (`max_clauses`, default 3^n) raises
`RuntimeError` (`dep/constants.yaml`, `const.max_clauses`). Worst-case cost
O(9^n) pair inspections; this exponential bound is a property of resolution
and is declared here. The engine is sound (every derived clause follows from
its parents) and refutation-complete for propositional CNF (saturation to a
fixpoint decides satisfiability). Claim status: `empirical`
(`dep/claims.yaml`, `emp.resolution_engine`); the engine itself is not
formally verified, and every derivation is machine-checked against the
clause-level criterion of `check_derivation` by the test suite.

## Invariants

1. Every `input` step's clause is a premise; every `resolution` step's clause
   is a subset of the parent union minus the eliminated literal pair
   (`check_derivation` verifies both, and the tests assert it for every
   produced derivation).
2. The engine never reports `unknown`: saturation either derives the empty
   clause or reaches a fixpoint without it.
3. CNF output ordering is a function of the input formula alone.

## Integration Points

Depends on: Python 3.12 standard library. Depended on by: the demo pipeline
(stage 3), the SMT cross-check test, `tautology`. The Lean bridge emits tasks
decided here, and Lean re-proves them independently
(`doc/LeanBridge.md`); the engine's derivation is a search hint, not a
trusted input.

## Known Limitations

Propositional logic only: no quantifiers, no theories, no unification. The
CNF conversion can be exponential in the formula size (distribution), and the
saturation is exponential in the variable count; both bounds are declared,
not optimized. Tautological clauses are not filtered. The engine decides
satisfiability of the input clause set; entailment holds iff the negated
goal refutes against the premise clauses, which is the only supported query.
