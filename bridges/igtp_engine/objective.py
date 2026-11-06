"""Discrete objective components: geodesic energy, constraint potential,
description-length regularizer.

This module is the runtime analog of `IGTP.ObjectiveComponents` in the Lean
formal core. The correspondence is:

  Lean field          this module
  ----------------    -----------------------------------------------
  metric p v v        edge weight w(e) (unit velocity along e)
  geodesicEnergy      DiscreteObjective.energy: (1/2) * w(e)
  smtPotential        EdgeObjective.potential V(e)
  descriptionLength   EdgeObjective.description K(e)
  discreteAction      discrete_action(path): sum of edge_weight over path

All values are exact Fractions; the per-edge nonnegativity discharged in Lean
by `smt_nonneg` / `dl_nonneg` is enforced here by validation at construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .manifold import ConceptGraph


@dataclass(frozen=True)
class EdgeObjective:
    """Objective components attached to one edge traversal."""

    metric: Fraction
    potential: Fraction
    description: Fraction

    def __post_init__(self) -> None:
        for name in ("metric", "potential", "description"):
            value = getattr(self, name)
            if not isinstance(value, Fraction) or value < 0:
                raise ValueError(f"{name} must be a Fraction >= 0")


class DiscreteObjective:
    """Combines the three components into one edge weight.

    edge_weight(e) = (1/2) * metric(e) + potential(e) + description(e).

    The factor (1/2) matches `IGTP.geodesicEnergy` with unit velocity.
    """

    @staticmethod
    def energy(metric: Fraction) -> Fraction:
        """Geodesic energy of a unit-velocity edge traversal."""
        return Fraction(1, 2) * metric

    @staticmethod
    def edge_weight(edge: EdgeObjective) -> Fraction:
        return DiscreteObjective.energy(edge.metric) + edge.potential + edge.description


def discrete_action(
    graph: ConceptGraph, objective: dict[tuple[str, str], EdgeObjective], path: list[str]
) -> Fraction:
    """Discrete action of a path: the sum of combined edge weights.

    This mirrors `IGTP.discreteAction`, with the path's time steps realized by
    its edges. Raises KeyError if a traversed edge has no declared objective.
    """
    total = Fraction(0)
    for u, v in zip(path, path[1:]):
        edge = objective.get((u, v)) or objective.get((v, u))
        if edge is None:
            raise KeyError(f"no objective declared for edge ({u}, {v})")
        total += DiscreteObjective.edge_weight(edge)
    return total
