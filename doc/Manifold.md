# MetricManifold

## Abstract

`IGTP.MetricManifold` defines the abstract carrier of the IGTP state space:
a type of points with a tangent family, a real-valued metric component
function, a real-valued Ricci component function, and one condition,
diagonal positive semidefiniteness. It takes no input beyond the carrier
type; it produces the interface on which `IGTP.Objective` and
`IGTP.RicciFlow` are stated.

## Formal Definitions

Lean 4 (IGTP/Manifold.lean):

```lean
class MetricManifold (M : Type*) where
  Tangent : M → Type*
  metric : ∀ p : M, Tangent p → Tangent p → ℝ
  metric_nonneg : ∀ (p : M) (v : Tangent p), 0 ≤ metric p v v
  ricci : ∀ p : M, Tangent p → Tangent p → ℝ

def PathVelocity (γ : ℝ → M) : Type _ := ∀ t : ℝ, Tangent (γ t)

noncomputable def geodesicEnergy (γ : ℝ → M) (v : PathVelocity γ) (t : ℝ) : ℝ :=
  (1 / 2 : ℝ) * metric (γ t) (v t) (v t)
```

`Tangent p` is the type of tangent vectors at `p`; `metric p u v` is the
metric-tensor component `g_p(u, v)`; `ricci p u v` is the Ricci component
`R_p(u, v)`, declared data rather than a tensor derived from `metric`.

## Algorithm

The module contains no algorithm. It contains one proved statement:
`geodesicEnergy_nonneg`, the nonnegativity of the energy density from the
diagonal condition, proved by `mul_nonneg` applied to the positivity of
`1/2` and the class condition. Axioms: the standard Mathlib set
(propext, Classical.choice, Quot.sound); see `dep/out/axioms/`.

## Invariants

1. For every point `p` and tangent vector `v`: `metric p v v ≥ 0`.
2. Every field of the class is used by a definition or a theorem in the
   package; the class carries no unused data.
3. The energy density is defined only through the class fields; no other
   structure of `M` is referenced.

## Integration Points

Depends on: Mathlib @ 4bbdccd9c5f862bf90ff12f0a9e2c8be032b9a84
(ordered field arithmetic). Depended on by: `IGTP.Objective`,
`IGTP.RicciFlow` (import IGTP.Manifold). Cross-language: the discrete analog
is `ConceptGraph` in `doc/ConceptGraph.md`; the correspondence of fields is
tabulated in `doc/Objective.md`.

## Known Limitations

The interface enforces no bilinearity or symmetry of `metric`, no relation
between `ricci` and `metric`, and no topology or smooth structure on `M`.
Consequently no differential-geometric theorem (geodesic equations, curvature
bounds, flow existence) can be stated against this interface in the current
package. `PathVelocity` is declared data; no coherence between a velocity
assignment and an analytic derivative is assumed or enforced. These
obligations are listed in `dep/manifest.yaml` as future conformance work.
