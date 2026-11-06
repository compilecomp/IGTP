"""Deterministic best-first geodesic search over the concept manifold.

The search minimizes the combined discrete objective (energy + constraint
potential + description length) between a source and a target concept. It is
Dijkstra's algorithm over the combined weights with id-based tie-breaking, so
the returned path and energy are a deterministic function of the input.

Complexity: O((V + E) log V) time, O(V) space, on exact rational weights.
The worst-case search cost is polynomial in the graph size; the conjecture
that the corresponding cost on the smooth manifold is polynomial in the
*proof* size is registered as `conj.search_complexity` in dep/claims.yaml and
is not established by this module.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from fractions import Fraction

from .manifold import ConceptGraph
from .objective import EdgeObjective, DiscreteObjective


@dataclass(frozen=True)
class PathResult:
    """Outcome of a geodesic search.

    Attributes:
      path: node ids from source to target, both included.
      energy: the discrete action of the path (exact rational).
      expanded: number of nodes finalized by the search (diagnostic only;
        excluded from golden comparisons).
    """

    path: list[str]
    energy: Fraction
    expanded: int


def geodesic_search(
    graph: ConceptGraph,
    objective: dict[tuple[str, str], EdgeObjective],
    source: str,
    target: str,
) -> PathResult:
    """Best-first search from source to target under the combined objective.

    Raises KeyError if source or target is not a declared node, or if the
    target is unreachable.
    """
    if not graph.has_node(source):
        raise KeyError(f"source {source!r} is not a declared node")
    if not graph.has_node(target):
        raise KeyError(f"target {target!r} is not a declared node")

    def weight(u: str, v: str) -> Fraction:
        edge = objective.get((u, v)) or objective.get((v, u))
        if edge is None:
            raise KeyError(f"no objective declared for edge ({u}, {v})")
        return DiscreteObjective.edge_weight(edge)

    dist: dict[str, Fraction] = {source: Fraction(0)}
    prev: dict[str, str] = {}
    heap: list[tuple[Fraction, str]] = [(Fraction(0), source)]
    done: set[str] = set()
    expanded = 0
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        expanded += 1
        if u == target:
            break
        for v in graph.neighbors(u):
            nd = d + weight(u, v)
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    if target not in done:
        raise KeyError(f"target {target!r} is unreachable from {source!r}")

    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    path.reverse()

    total = Fraction(0)
    for u, v in zip(path, path[1:]):
        total += weight(u, v)
    return PathResult(path=path, energy=total, expanded=expanded)
