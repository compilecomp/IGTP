/-
Copyright (c) 2026 the IGTP contributors. Released under the Apache License 2.0.
-/
import Mathlib

/-!
# IGTP.MetricManifold

The abstract carrier of the IGTP state space: a type of points, a family of tangent
spaces, a real-valued metric-tensor component function, and a real-valued Ricci
component function, subject to one condition: positive semidefiniteness of the
metric along the diagonal.

The interface is data-only. No topological, smoothness, or bilinearity conditions
are enforced; the obligations that this choice generates are recorded in
`doc/Manifold.md` and in `dep/manifest.yaml`. Every field of the class is used by
a definition or a theorem in this package.
-/

namespace IGTP

/-- Abstract metric-manifold interface of IGTP.

A `MetricManifold M` carries, for each point `p : M`:
* a tangent type `Tangent p`,
* a real-valued metric-tensor component function `metric p`,
* the diagonal positive semidefiniteness condition `metric_nonneg p`,
* a real-valued Ricci component function `ricci p` (declared data, not derived
  from `metric`; see `doc/Manifold.md`, Known Limitations). -/
class MetricManifold (M : Type*) where
  /-- The tangent space at point `p`. -/
  Tangent : M → Type*
  /-- The metric-tensor component function `g_p(u, v) : ℝ`. -/
  metric : ∀ p : M, Tangent p → Tangent p → ℝ
  /-- Diagonal positive semidefiniteness: `g_p(v, v) ≥ 0` for every `p` and `v`. -/
  metric_nonneg : ∀ (p : M) (v : Tangent p), 0 ≤ metric p v v
  /-- The Ricci-tensor component function `R_p(u, v) : ℝ`, as declared data. -/
  ricci : ∀ p : M, Tangent p → Tangent p → ℝ

export MetricManifold (Tangent metric metric_nonneg ricci)

variable {M : Type*} [MetricManifold M]

/-- A velocity assignment along a path `γ : ℝ → M`: declared data associating to
each time `t` a tangent vector at `γ t`.

No coherence between this assignment and any analytic derivative is assumed by
this package; the coherence obligation is listed as future work in
`doc/Manifold.md`. -/
def PathVelocity (γ : ℝ → M) : Type _ := ∀ t : ℝ, Tangent (γ t)

/-- Geodesic energy density of a path at time `t`:
`E(γ, v, t) = (1/2) · g_{γ(t)}(v(t), v(t))`. -/
noncomputable def geodesicEnergy (γ : ℝ → M) (v : PathVelocity γ) (t : ℝ) : ℝ :=
  (1 / 2 : ℝ) * metric (γ t) (v t) (v t)

/-- The geodesic energy density is nonnegative. This is the one-condition
consequence of `MetricManifold.metric_nonneg` used by `IGTP.discreteAction_nonneg`. -/
theorem geodesicEnergy_nonneg (γ : ℝ → M) (v : PathVelocity γ) (t : ℝ) :
    0 ≤ geodesicEnergy γ v t :=
  mul_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2) (metric_nonneg (γ t) (v t))

/-- Non-vacuity witness for `MetricManifold`: the one-point model `M = Unit` with
`Tangent _ = ℝ`, `g(u, v) = u * v` and `R = 0`. The diagonal condition holds
because `u ^ 2 ≥ 0`. -/
instance instMetricManifoldUnit : MetricManifold Unit where
  Tangent _ := ℝ
  metric _ u _ := u ^ 2
  metric_nonneg _ u := sq_nonneg u
  ricci _ _ _ := 0

end IGTP
