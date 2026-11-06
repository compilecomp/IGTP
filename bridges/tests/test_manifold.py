"""Tests for the concept manifold (exact arithmetic, determinism, invariants)."""

import pytest
from fractions import Fraction

from igtp_engine.manifold import ConceptGraph

F = Fraction


@pytest.fixture
def diamond() -> ConceptGraph:
    graph = ConceptGraph()
    for n in ["a", "b", "c", "d"]:
        graph.add_node(n, "test")
    graph.add_edge("a", "b", F(1))
    graph.add_edge("a", "c", F(4))
    graph.add_edge("b", "d", F(1))
    graph.add_edge("c", "d", F(1))
    return graph


def test_distances_exact(diamond: ConceptGraph) -> None:
    dist = diamond.distances("a")
    assert dist["d"] == F(2)
    assert dist["c"] == F(3)
    assert dist["a"] == F(0)


def test_shortest_path_and_symmetry(diamond: ConceptGraph) -> None:
    path, cost = diamond.shortest_path("a", "d")
    assert path == ["a", "b", "d"]
    assert cost == F(2)
    path_rev, cost_rev = diamond.shortest_path("d", "a")
    assert path_rev == ["d", "b", "a"]
    assert cost_rev == F(2)


def test_edge_weight_symmetric(diamond: ConceptGraph) -> None:
    assert diamond.edge_weight("a", "b") == diamond.edge_weight("b", "a") == F(1)


def test_negative_weight_rejected() -> None:
    graph = ConceptGraph()
    graph.add_node("x", "test")
    graph.add_node("y", "test")
    with pytest.raises(ValueError):
        graph.add_edge("x", "y", F(-1))


def test_float_weight_rejected() -> None:
    graph = ConceptGraph()
    graph.add_node("x", "test")
    graph.add_node("y", "test")
    with pytest.raises(ValueError):
        graph.add_edge("x", "y", 1.0)  # type: ignore[arg-type]


def test_unknown_endpoint_rejected() -> None:
    graph = ConceptGraph()
    graph.add_node("x", "test")
    with pytest.raises(ValueError):
        graph.add_edge("x", "y", F(1))


def test_duplicate_node_rejected() -> None:
    graph = ConceptGraph()
    graph.add_node("x", "test")
    with pytest.raises(ValueError):
        graph.add_node("x", "other")


def test_unreachable_raises(diamond: ConceptGraph) -> None:
    diamond.add_node("z", "test")
    with pytest.raises(KeyError):
        diamond.shortest_path("a", "z")
