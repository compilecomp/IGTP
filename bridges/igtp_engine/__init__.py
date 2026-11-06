"""IGTP reference engine: discrete semantic manifold, objective, and solver bridges.

Modules:
  manifold      finite weighted concept graph (discrete metric-space analog)
  objective     discrete geodesic energy, constraint potential, description length
  search        deterministic best-first geodesic search over the manifold
  resolution    propositional resolution engine (ATP component)
  smt_bridge    z3 SMT bridge with declared finite timeouts (SMT component)
  lean_bridge   Lean 4 certificate emitter (ITP component)
  pipeline      end-to-end demo pipeline shared by experiments and tests

Claim statuses of the engine components are recorded in dep/claims.yaml:
the engines are `empirical`, supported by the test suite and the demo artifact;
they are not machine-checked.
"""

__version__ = "0.1.0"
