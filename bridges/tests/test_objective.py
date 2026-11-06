"""Tests for the discrete objective components."""

from fractions import Fraction

import pytest

from igtp_engine.manifold import ConceptGraph
from igtp_engine.objective import DiscreteObjective, EdgeObjective, discrete_action

F = Fraction


def test_energy_is_half_metric() -> None:
    assert DiscreteObjective.energy(F(3)) == F(3, 2)
    assert DiscreteObjective.energy(F(0)) == F(0)


def test_edge_weight_combination() -> None:
    edge = EdgeObjective(metric=F(2), potential=F(1), description=F(1, 2))
    assert DiscreteObjective.edge_weight(edge) == F(1) + F(1) + F(1, 2)


def test_negative_component_rejected() -> None:
    with pytest.raises(ValueError):
        EdgeObjective(metric=F(1), potential=F(-1), description=F(0))


def test_discrete_action_matches_manual_sum() -> None:
    graph = ConceptGraph()
    for n in ["u", "v", "w"]:
        graph.add_node(n, "test")
    graph.add_edge("u", "v", F(2))
    graph.add_edge("v", "w", F(4))
    objective = {
        ("u", "v"): EdgeObjective(F(2), F(1), F(0)),
        ("v", "w"): EdgeObjective(F(4), F(0), F(1)),
    }
    action = discrete_action(graph, objective, ["u", "v", "w"])
    assert action == (F(1) + F(1) + F(0)) + (F(2) + F(0) + F(1))


def test_discrete_action_symmetric_objective_lookup() -> None:
    graph = ConceptGraph()
    for n in ["u", "v"]:
        graph.add_node(n, "test")
    graph.add_edge("u", "v", F(2))
    objective = {("v", "u"): EdgeObjective(F(2), F(0), F(0))}
    assert discrete_action(graph, objective, ["u", "v"]) == F(1)


def test_missing_objective_raises() -> None:
    graph = ConceptGraph()
    for n in ["u", "v"]:
        graph.add_node(n, "test")
    graph.add_edge("u", "v", F(2))
    with pytest.raises(KeyError):
        discrete_action(graph, {}, ["u", "v"])
