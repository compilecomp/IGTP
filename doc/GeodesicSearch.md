# GeodesicSearch

## Abstract

`geodesic_search` (bridges/igtp_engine/search.py) finds a least combined-cost
path between two concepts of a `ConceptGraph` under the discrete objective.
It takes a graph, an edge-objective table, a source, and a target; it
produces the path, its exact energy, and a diagnostic expansion count.

## Formal Definitions

Python 3.12:

```python
@dataclass(frozen=True)
class PathResult:
    path: list[str]        # source .. target, both included
    energy: Fraction       # exact rational; sum of combined edge weights
    expanded: int          # diagnostic only; excluded from golden comparisons

def geodesic_search(
    graph: ConceptGraph,
    objective: dict[tuple[str, str], EdgeObjective],
    source: str,
    target: str,
) -> PathResult
```

Combined weight of one edge traversal
(`DiscreteObjective.edge_weight`): `(1/2) * metric + potential +
description`, all exact `Fraction`s. The factor 1/2 matches
`IGTP.geodesicEnergy` at unit velocity.

## Algorithm

Dijkstra's algorithm over the combined weights: a binary heap keyed by
(cost, node id), neighbor iteration sorted by node id. On finalizing the
target the path is reconstructed from predecessor records and its energy is
recomputed from the declared objectives rather than taken from the distance
table. Time complexity O((V + E) log V); space O(V). Assumptions: every
traversed edge has a declared objective (else `KeyError`); the target is
reachable (else `KeyError`). Determinism: the output is a function of the
inputs alone; two runs on identical inputs produce identical paths and
energies (test `test_search_is_deterministic`).

The search cost on the demo graph is polynomial in the graph size. The
design target that the corresponding cost for proof search on the smooth
manifold is polynomial in the instance size is `conj.search_complexity`,
status `conjectural`; this module establishes no claim about proof search
complexity.

## Invariants

1. The reported energy equals the sum of combined weights along the reported
   path, computed by an independent second pass.
2. The path is simple in cost: no strictly cheaper path exists on the
   declared graph and objective (Dijkstra correctness; verified against
   `ConceptGraph.shortest_path` in the test suite for the pure-metric case).
3. Source and target are declared nodes; violation raises `KeyError`.

## Integration Points

Depends on: `ConceptGraph` (manifold.py), `EdgeObjective` and
`DiscreteObjective` (objective.py). Depended on by: the demo pipeline
(pipeline.py, stage 2) and the test suite. Cross-language: the search
realizes Goal 1 of `doc/DesignGoals.md` at the discrete level; the Lean
formal core contains no search procedure.

## Known Limitations

The search minimizes the declared combined weight only; constraint
consistency (the SMT component) enters as a fixed per-edge penalty, not as a
call to a solver during search. No heuristic guidance, no bidirectional
search, no pruning beyond Dijkstra's. The expansion count is diagnostic and
excluded from golden artifacts; it must not be used as a performance claim.
