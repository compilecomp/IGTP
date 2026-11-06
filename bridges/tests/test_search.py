"""Tests for the geodesic search: optimality, determinism, error handling."""

from fractions import Fraction

import pytest

from igtp_engine.manifold import ConceptGraph
from igtp_engine.objective import EdgeObjective
from igtp_engine.search import geodesic_search
from igtp_engine.pipeline import build_demo_graph, build_demo_objective

F = Fraction


def _identity_objective(graph: ConceptGraph) -> dict[tuple[str, str], EdgeObjective]:
    return {(u, v): EdgeObjective(w, F(0), F(0)) for u, v, w in graph.edges()}


def test_search_finds_expected_optimum_on_demo_graph() -> None:
    """Hand-computed optimum: the constraint potential reroutes the path."""
    graph = build_demo_graph()
    objective = build_demo_objective()
    result = geodesic_search(graph, objective, "logic:premise", "logic:conclusion")
    assert result.path == ["logic:premise", "logic:elimination", "logic:tautology", "logic:conclusion"]
    assert result.energy == F(5, 2)


def test_search_arith_to_certificate() -> None:
    graph = build_demo_graph()
    objective = build_demo_objective()
    result = geodesic_search(graph, objective, "arith:half", "meta:certificate")
    assert result.path == ["arith:half", "logic:tautology", "meta:goal", "meta:certificate"]
    assert result.energy == F(2)


def test_search_is_deterministic() -> None:
    graph = build_demo_graph()
    objective = build_demo_objective()
    first = geodesic_search(graph, objective, "top:connected", "meta:goal")
    second = geodesic_search(graph, objective, "top:connected", "meta:goal")
    assert first.path == second.path
    assert first.energy == second.energy


def test_search_matches_dijkstra_distance_without_potential() -> None:
    graph = build_demo_graph()
    objective = _identity_objective(graph)
    result = geodesic_search(graph, objective, "logic:premise", "meta:certificate")
    _, cost = graph.shortest_path("logic:premise", "meta:certificate")
    assert result.energy * 2 == cost


def test_search_unknown_node_raises() -> None:
    graph = build_demo_graph()
    objective = _identity_objective(graph)
    with pytest.raises(KeyError):
        geodesic_search(graph, objective, "nope", "meta:goal")


def test_search_unreachable_raises() -> None:
    graph = build_demo_graph()
    graph.add_node("isolated", "test")
    objective = _identity_objective(graph)
    with pytest.raises(KeyError):
        geodesic_search(graph, objective, "logic:premise", "isolated")


def test_search_missing_objective_raises() -> None:
    graph = build_demo_graph()
    with pytest.raises(KeyError):
        geodesic_search(graph, {}, "logic:premise", "meta:goal")
