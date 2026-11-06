"""Finite weighted concept graph: the discrete analog of the IGTP state space.

The smooth `MetricManifold` interface of the Lean formal core is realized here
by a finite undirected graph with nonnegative rational edge weights. The path
metric is the least-weight path distance; the geodesic energy of traversing an
edge with unit velocity is one half of its weight.

Every weight is a `Fraction`: arithmetic is exact (class `exact` in the
arithmetic classification of DEP&CC 2.0, Chapter 18.1). No floating-point
value enters any load-bearing computation.

Complexity: Dijkstra distances run in O((V + E) log V) on a binary heap, with
V the node count and E the edge count of the stored (undirected) graph.
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Node:
    """A concept on the manifold: an identifier and a domain tag."""

    id: str
    domain: str


class ConceptGraph:
    """Finite undirected weighted graph with exact rational weights.

    Invariants:
      I1. Every stored weight is a Fraction greater than or equal to 0.
      I2. Adjacency is symmetric: (u, v) and (v, u) denote the same edge.
      I3. Every edge endpoint is a declared node.
    Violation of any invariant raises ValueError at mutation time.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._adj: dict[str, dict[str, Fraction]] = {}

    def add_node(self, node_id: str, domain: str) -> None:
        if node_id in self._nodes:
            raise ValueError(f"node already declared: {node_id}")
        self._nodes[node_id] = Node(node_id, domain)
        self._adj[node_id] = {}

    def add_edge(self, u: str, v: str, weight: Fraction) -> None:
        """Add the undirected edge {u, v} with the given nonnegative weight."""
        if u not in self._nodes or v not in self._nodes:
            raise ValueError("edge endpoints must be declared nodes")
        if not isinstance(weight, Fraction) or weight < 0:
            raise ValueError("edge weight must be a Fraction >= 0")
        self._adj[u][v] = weight
        self._adj[v][u] = weight

    def node(self, node_id: str) -> Node:
        return self._nodes[node_id]

    def node_ids(self) -> list[str]:
        """Declared node ids, sorted. Deterministic iteration order."""
        return sorted(self._nodes)

    def has_node(self, node_id: str) -> bool:
        return node_id in self._nodes

    def edge_weight(self, u: str, v: str) -> Fraction:
        if v not in self._adj[u]:
            raise KeyError(f"no edge between {u} and {v}")
        return self._adj[u][v]

    def neighbors(self, u: str) -> list[str]:
        """Neighbors of u, sorted by id. Deterministic iteration order."""
        return sorted(self._adj[u])

    def edges(self) -> list[tuple[str, str, Fraction]]:
        """All undirected edges as (u, v, w) with u < v, sorted."""
        out = []
        for u in self.node_ids():
            for v in self.neighbors(u):
                if u < v:
                    out.append((u, v, self._adj[u][v]))
        return out

    def distances(self, source: str) -> dict[str, Fraction]:
        """Least-weight path distances from source (Dijkstra, exact arithmetic).

        Unreachable nodes are absent from the result. O((V + E) log V).
        """
        dist: dict[str, Fraction] = {source: Fraction(0)}
        heap: list[tuple[Fraction, str]] = [(Fraction(0), source)]
        done: set[str] = set()
        while heap:
            d, u = heapq.heappop(heap)
            if u in done:
                continue
            done.add(u)
            for v in self.neighbors(u):
                nd = d + self._adj[u][v]
                if v not in dist or nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        return dist

    def shortest_path(self, source: str, target: str) -> tuple[list[str], Fraction]:
        """Least-weight path and its cost from source to target.

        Returns (path, cost) with path[0] == source and path[-1] == target.
        Raises KeyError if target is unreachable. Tie-breaking is by node id,
        which makes the returned path a deterministic function of the graph.
        """
        dist: dict[str, Fraction] = {source: Fraction(0)}
        prev: dict[str, str] = {}
        heap: list[tuple[Fraction, str]] = [(Fraction(0), source)]
        done: set[str] = set()
        while heap:
            d, u = heapq.heappop(heap)
            if u in done:
                continue
            done.add(u)
            if u == target:
                break
            for v in self.neighbors(u):
                nd = d + self._adj[u][v]
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
        return path, dist[target]
