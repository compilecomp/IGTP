# Design Goals

## Abstract

This document records the five design goals of the Information-Geometric
Theorem Proving (IGTP) program and their epistemic status in this repository.
It is a DEP-2 document: it contains no load-bearing inference, and every claim
it states carries a status from `dep/claims.yaml`. The formal content of the
goals lives in the Lean modules under `IGTP/` and the reference engine under
`bridges/`.

## Formal Definitions

The five goals constrain one object: the pair (state space, objective).

1. State space. A `MetricManifold M` (IGTP/Manifold.lean): a carrier type of
   points, a tangent family, a real-valued metric component function, a
   real-valued Ricci component function, and diagonal positive
   semidefiniteness. The discrete realization is a finite weighted graph
   (`bridges/igtp_engine/manifold.py`).
2. Objective. `ObjectiveComponents` (IGTP/Objective.lean): geodesic energy
   E, a constraint potential V (SMT component), and a description-length
   regularizer K (ITP component), combined additively into the discrete
   action S.

## The goals, with their status

Goal 1, Navigation. Syntactic theorem provers explore proof trees without
semantic guidance, and their worst-case cost is exponential in the instance
size. IGTP replaces unguided branching by search under a semantic objective:
the solver advances along least-cost paths of the combined objective on the
state space. Implemented: `GeodesicSearch` (bridges/igtp_engine/search.py),
Dijkstra under exact rational weights, O((V + E) log V). Status of the
corresponding design target for smooth-manifold proof search: `conjectural`
(`dep/claims.yaml`, `conj.search_complexity`); no complexity separation is
proved in this repository.

Goal 2, Minimal-complexity selection. Proofs produced by saturating provers
can be large relative to the mathematical content of their conclusion. IGTP
adds a description-length term K to the objective, so that among searched
candidate paths the solver prefers those with lower declared description
length. Implemented: the K component of the objective, nonnegative by
construction. Status of the design target "the selected path has minimal
algorithmic complexity among candidates": `conjectural`
(`conj.kolmogorov_minimality`); Kolmogorov complexity is uncomputable, K is a
declared nonnegative proxy, and no minimality theorem exists here.

Goal 3, Division of labor between human and machine. In current interactive
provers the human supplies the creative steps and the machine verifies
bookkeeping. IGTP models the human contribution as boundary conditions: the
human fixes anchor points (time, point) on the proof path, and the machine
interpolates a verified path between them. Implemented: `SatisfiesAnchor`,
`AnchorSet`, and the existence theorem for consistent anchor sets
(IGTP/Boundary.lean, `res.anchors_exist`). The interpolation objective and
the automation that fills anchors are future work.

Goal 4, Unified state space. A prover for one domain rarely shares state
with a prover for another. IGTP places all domains as nodes of one state
space, so that the distance between concepts of different domains is
measured by the same metric data as distances within a domain. Implemented:
the demo manifold carries logic, arithmetic, topology, and meta nodes on one
graph; search crosses domains without solver translation
(`experiments/code/run_demo.py`). This is an implementation of the interface,
not a result about cross-domain transfer; no such result is claimed.

Goal 5, Structure-guided conjecture generation. The long-term target is that
defects of the state-space geometry (regions where the metric data is
inconsistent with the declared library) indicate locations where theorems are
missing. Status: `conjectural` (`conj.curvature_discovery`); this repository
contains no implementation and no evidence for this target.

## Target end state

The declared end state of the program is an engine that maps a conjecture to
a location on the state space, smooths the space to focus search, generates a
kernel-checked proof along a least-cost path, and reports the anchors and the
path structure so a reader can reconstruct the argument. Each of the four
stages maps to a component in this repository (mapping: `ConceptGraph`;
smoothing: `IsRicciFlow`, definition only; generation: `GeodesicSearch` plus
`ResolutionEngine` plus `SMTBridge`; reporting: `LeanBridge`), and each stage
carries the status of its component: the formal core is machine-checked, the
engines are `empirical`, and the smoothing-to-search connection is
`conjectural`.

## Invariants

1. No engine output is trusted without kernel checking or an independent
   cross-check; claim statuses in `dep/claims.yaml` record the trust path.
2. Every claim in the README and in `doc/` maps to a result ID in
   `dep/claims.yaml` (Law 12: no claim inflation).
3. Components with status `conjectural` are never dependencies of components
   with status `complete` (Rule DEP-LINT-STATUS-CONTAMINATION).

## Integration Points

Depends on: every component document in `doc/`; `dep/claims.yaml` for the
status vocabulary. Depended on by: `README.md` (claims sections).

## Known Limitations

The complexity targets of Goals 1 and 2 are unproved. The manifold interface
carries no topological or smoothness conditions, so no differential-geometric
theorem can be stated against it yet. The K component is a proxy; no
statement about Kolmogorov complexity is possible against it. Goal 5 has no
implementation. Independent cold reads of the DEP-0 results are scheduled in
`dep/manifest.yaml` and have not been performed.
