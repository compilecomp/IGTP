# ConceptGraph

## Abstract

`ConceptGraph` (bridges/igtp_engine/manifold.py) is the finite, discrete
realization of the IGTP state space: an undirected graph with exact
nonnegative rational edge weights. It takes node and edge declarations; it
produces least-weight distances and paths via Dijkstra under exact
arithmetic.

## Formal Definitions

Python 3.12 (dataclasses; exact `fractions.Fraction` weights):

```python
@dataclass(frozen=True)
class Node:
    id: str
    domain: str

class ConceptGraph:
    def add_node(self, node_id: str, domain: str) -> None
    def add_edge(self, u: str, v: str, weight: Fraction) -> None
    def edge_weight(self, u: str, v: str) -> Fraction
    def neighbors(self, u: str) -> list[str]          # sorted
    def distances(self, source: str) -> dict[str, Fraction]
    def shortest_path(self, source: str, target: str) -> tuple[list[str], Fraction]
```

Domain constraint (`dep/conventions.yaml`, `conv.graph`): the graph is
finite, simple, undirected, loopless; weights are exact nonnegative
rationals. Floating-point weights are rejected at mutation time.

## Algorithm

`distances` and `shortest_path` run Dijkstra's algorithm on a binary heap
with exact `Fraction` keys. Neighbor iteration is sorted by node id and
tie-breaking is by node id, so both outputs are a deterministic function of
the declared graph. Time complexity O((V + E) log V); space O(V + E), with V
nodes and E stored edges. Assumptions: weights are nonnegative (validated on
insertion); the source is a declared node (validated). Unreachable targets
raise `KeyError`; distances omit unreachable nodes.

## Invariants

1. I1: every stored weight is a `Fraction >= 0`.
2. I2: adjacency is symmetric; `(u, v)` and `(v, u)` denote the same edge.
3. I3: every edge endpoint is a declared node.
4. Violation of I1-I3 raises `ValueError` at mutation time, before any query
   can observe it.

## Integration Points

Depends on: Python 3.12 standard library (`heapq`, `fractions`,
`dataclasses`). Depended on by: `DiscreteObjective` and `geodesic_search`
(objective.py, search.py), the demo pipeline (pipeline.py), and the test
suite (bridges/tests). Cross-language: the field correspondence with the Lean
`MetricManifold` interface is tabulated in `doc/Objective.md`; the graph is a
metric-space analog, not a smooth manifold, and no Riemannian theorem is
claimed about it.

## Known Limitations

The graph is finite and static; no dynamic updates, no negative or
floating-point weights, no multiedges. Dijkstra requires nonnegative weights;
the validation makes a violation impossible rather than detected after the
fact. The path metric of a graph is not a Riemannian metric; the
correspondence is an analogy recorded for orientation, and its limits are
stated in `doc/DesignGoals.md`.
