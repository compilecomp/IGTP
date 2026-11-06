"""End-to-end reference pipeline shared by the demo experiment and the tests.

Pipeline stages, matching the IGTP design goals:
  1. Semantic mapping:   build the finite concept manifold and the objective.
  2. Search:             geodesic search between concept pairs (goal 1).
  3. Derivation:         propositional resolution on the logic tasks (goal 2,
                         exact rational bookkeeping of derivation cost).
  4. Cross-check:        z3 with a declared finite timeout (policy P1-P4).
  5. Certificate:        Lean 4 emission, kernel-checked in CI (goal 3).

The output of `run_pipeline` is a JSON-serializable dictionary with no wall
clock times: identical inputs produce identical bytes. Wall-clock timings are
collected by the demo runner separately and are informational only.
"""

from __future__ import annotations

from fractions import Fraction

import z3

from . import resolution, search, smt_bridge
from .lean_bridge import LeanTask
from .manifold import ConceptGraph
from .objective import EdgeObjective

F = Fraction


def build_demo_graph() -> ConceptGraph:
    """The demo concept manifold: 12 concepts over 4 domains."""
    graph = ConceptGraph()
    nodes = [
        ("logic:premise", "logic"),
        ("logic:q", "logic"),
        ("logic:r", "logic"),
        ("logic:conclusion", "logic"),
        ("logic:elimination", "logic"),
        ("logic:tautology", "logic"),
        ("arith:order", "arithmetic"),
        ("arith:half", "arithmetic"),
        ("top:connected", "topology"),
        ("top:pathspace", "topology"),
        ("meta:goal", "meta"),
        ("meta:certificate", "meta"),
    ]
    for node_id, domain in nodes:
        graph.add_node(node_id, domain)
    edges = [
        ("logic:premise", "logic:elimination", F(1)),
        ("logic:q", "logic:elimination", F(1)),
        ("logic:q", "logic:r", F(2)),
        ("logic:r", "logic:conclusion", F(2)),
        ("logic:elimination", "logic:conclusion", F(3)),
        ("logic:elimination", "logic:tautology", F(2)),
        ("logic:tautology", "logic:conclusion", F(1)),
        ("arith:order", "arith:half", F(1)),
        ("arith:half", "logic:tautology", F(2)),
        ("arith:order", "top:connected", F(4)),
        ("top:connected", "top:pathspace", F(1)),
        ("top:pathspace", "logic:tautology", F(3)),
        ("logic:tautology", "meta:goal", F(1)),
        ("meta:goal", "meta:certificate", F(1)),
        ("logic:conclusion", "meta:goal", F(2)),
    ]
    for u, v, w in edges:
        graph.add_edge(u, v, w)
    return graph


def build_demo_objective() -> dict[tuple[str, str], EdgeObjective]:
    """Per-edge objective: energy is (1/2) * metric; V and K reroute search."""
    objective: dict[tuple[str, str], EdgeObjective] = {}
    graph = build_demo_graph()
    for u, v, metric in graph.edges():
        potential = F(0)
        description = F(0)
        if {u, v} == {"logic:elimination", "logic:conclusion"}:
            potential = F(2)  # constraint check on this route fails
        if {u, v} == {"top:pathspace", "logic:tautology"}:
            potential = F(1)  # domain-crossing toll
        if {u, v} == {"logic:tautology", "logic:conclusion"}:
            description = F(1, 2)  # longer description of the shortcut
        objective[(u, v)] = EdgeObjective(metric, potential, description)
    return objective


def _frac(value: Fraction) -> str:
    """Deterministic serialization of a Fraction: 'n' or 'n/d'."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _formula_to_lean(f: tuple) -> str:
    kind = f[0]
    if kind == "var":
        return f[1]
    if kind == "not":
        return f"¬ {_formula_to_lean(f[1])}"
    if kind == "and":
        return f"({_formula_to_lean(f[1])} ∧ {_formula_to_lean(f[2])})"
    if kind == "or":
        return f"({_formula_to_lean(f[1])} ∨ {_formula_to_lean(f[2])})"
    if kind == "implies":
        return f"({_formula_to_lean(f[1])} → {_formula_to_lean(f[2])})"
    raise ValueError(f"unknown connective: {kind}")


def build_logic_tasks() -> list[dict]:
    """The propositional tasks: hypotheses, conclusion, and identifiers."""
    P, Q, R = resolution.var("P"), resolution.var("Q"), resolution.var("R")
    return [
        {
            "id": "logic:1",
            "vars": ["P", "Q", "R"],
            "hypotheses": [resolution.implies(P, Q), resolution.implies(Q, R), P],
            "conclusion": R,
            "search_source": "logic:premise",
            "search_target": "logic:conclusion",
        },
        {
            "id": "logic:2",
            "vars": ["P", "Q"],
            "hypotheses": [resolution.disj(P, Q), resolution.neg(P)],
            "conclusion": Q,
            "search_source": "top:connected",
            "search_target": "meta:goal",
        },
        {
            "id": "logic:3",
            "vars": ["P"],
            "hypotheses": [],
            "conclusion": resolution.disj(P, resolution.neg(P)),
            "search_source": "arith:half",
            "search_target": "meta:certificate",
        },
    ]


def run_pipeline() -> dict:
    """Run the full reference pipeline and return the serializable result."""
    graph = build_demo_graph()
    objective = build_demo_objective()
    tasks = build_logic_tasks()

    out: dict = {
        "engine_version": __import__("igtp_engine", fromlist=["__version__"]).__version__,
        "z3_version": smt_bridge.solver_version(),
        "graph": {
            "nodes": graph.node_ids(),
            "edges": [
                {"u": u, "v": v, "metric": _frac(w)} for u, v, w in graph.edges()
            ],
        },
        "tasks": [],
    }

    lean_tasks: list[LeanTask] = []
    for task in tasks:
        hyp_clauses: list[frozenset[str]] = []
        for hyp in task["hypotheses"]:
            hyp_clauses.extend(resolution.cnf(hyp))
        goal_clauses = resolution.cnf(resolution.negate(task["conclusion"]))
        outcome = resolution.saturate(hyp_clauses + goal_clauses)
        sound = resolution.check_derivation(hyp_clauses + goal_clauses, outcome.derivation)

        premises = z3.And(*[z3_formula(f) for f in task["hypotheses"]]) if task["hypotheses"] else z3.BoolVal(True)
        goal = z3_formula(task["conclusion"])
        smt = smt_bridge.check(z3.Not(z3.Implies(premises, goal)), timeout_ms=10000)

        search_result = search.geodesic_search(
            graph, objective, task["search_source"], task["search_target"]
        )

        out["tasks"].append(
            {
                "id": task["id"],
                "resolution": {
                    "refuted": outcome.refuted,
                    "derivation_steps": len(outcome.derivation),
                    "clause_count": outcome.clause_count,
                    "sound": sound,
                },
                "smt": {"status": smt.status.value},
                "search": {
                    "source": task["search_source"],
                    "target": task["search_target"],
                    "path": search_result.path,
                    "energy": _frac(search_result.energy),
                },
            }
        )
        lean_tasks.append(
            LeanTask(
                name="igtp_demo_" + task["id"].replace(":", "_"),
                prop_vars=task["vars"],
                hypotheses=[_formula_to_lean(h) for h in task["hypotheses"]],
                conclusion=_formula_to_lean(task["conclusion"]),
            )
        )

    from .lean_bridge import emit_lean_certificate

    out["lean_certificate_sha256"] = __import__("hashlib").sha256(
        emit_lean_certificate(lean_tasks).encode()
    ).hexdigest()
    return out


def z3_formula(f: tuple):
    """Convert a pipeline formula AST into a z3 boolean expression."""
    kind = f[0]
    if kind == "var":
        return z3.Bool(f[1])
    if kind == "not":
        return z3.Not(z3_formula(f[1]))
    if kind == "and":
        return z3.And(z3_formula(f[1]), z3_formula(f[2]))
    if kind == "or":
        return z3.Or(z3_formula(f[1]), z3_formula(f[2]))
    if kind == "implies":
        return z3.Implies(z3_formula(f[1]), z3_formula(f[2]))
    raise ValueError(f"unknown connective: {kind}")
