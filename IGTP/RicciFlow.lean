/-
Copyright (c) 2026 the IGTP contributors. Released under the Apache License 2.0.
-/
import IGTP.Manifold
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# IGTP.RicciFlow

The Ricci-flow equation `∂_t g = -2 R` for a time-dependent family of metric
component functions on a `MetricManifold`, and the statement that a
time-constant family is a Ricci flow exactly when the declared Ricci data
vanishes.

The equation is stated against the declared `ricci` data of the class, not
against a Ricci tensor derived from `metric`; deriving it is future work
(see `doc/RicciFlow.md`, Known Limitations).
-/

namespace IGTP

variable {M : Type*} [MetricManifold M]

/-- A time-dependent family of metric component functions on `M`:
for each time `s`, a component function `g_s(p, u, v) : ℝ`. -/
def MetricFamily (M : Type*) [_inst : MetricManifold M] : Type _ :=
  ℝ → ∀ p : M, Tangent p → Tangent p → ℝ

/-- The Ricci-flow equation at time `t`, point `p`, tangent vectors `u v`:
the time derivative of the component `g_s(p, u, v)` equals `-2 R_p(u, v)`. -/
def IsRicciFlowAt (g : MetricFamily M) (t : ℝ) (p : M) (u v : Tangent p) : Prop :=
  deriv (fun s : ℝ => g s p u v) t = -2 * ricci p u v

/-- The Ricci-flow equation on all of `M`, for all times and tangent vectors. -/
def IsRicciFlow (g : MetricFamily M) : Prop :=
  ∀ (t : ℝ) (p : M) (u v : Tangent p), IsRicciFlowAt g t p u v

/-- A time-constant metric family is a Ricci flow if and only if the declared
Ricci data vanishes identically.

Forward direction: the derivative of a constant is zero, so the flow equation
forces `-2 · R = 0`. Backward direction: substituting `R = 0` into the flow
equation gives the derivative of a constant, which is zero. -/
theorem isRicciFlow_const (g : ∀ p : M, Tangent p → Tangent p → ℝ) :
    IsRicciFlow (fun _ p => g p) ↔ ∀ (p : M) (u v : Tangent p), ricci p u v = 0 := by
  constructor
  · intro h p u v
    have h0 : deriv (fun _ : ℝ => g p u v) 0 = -2 * ricci p u v := h 0 p u v
    rw [deriv_const] at h0
    linarith
  · intro h t p u v
    have h0 : deriv (fun _ : ℝ => g p u v) t = 0 := by
      rw [deriv_const]
    exact (by rw [h0]; linarith [h p u v] :
      deriv (fun _ : ℝ => g p u v) t = -2 * ricci p u v)

/-- Non-vacuity witness for `isRicciFlow_const`: the one-point model with the
zero metric family and zero Ricci data satisfies the Ricci-flow equation. -/
example : IsRicciFlow (fun (_ : ℝ) (p : Unit) (u v : Tangent p) => (0 : ℝ)) := by
  intro t p u v
  show deriv (fun _ : ℝ => (0 : ℝ)) t = -2 * (0 : ℝ)
  rw [deriv_const]
  exact (mul_zero (-(2 : ℝ))).symm

end IGTP
