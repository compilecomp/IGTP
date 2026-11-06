/-
Copyright (c) 2026 the IGTP contributors. Released under the Apache License 2.0.
-/
import Mathlib

/-!
# IGTP.QuadraticModel

Natural-gradient descent on the one-dimensional quadratic model
`S(θ) = (c/2) · θ²` with Fisher-metric scalar `f > 0`.

The one-step descent theorems are proved exactly; the generalization to
multidimensional state spaces and to non-quadratic objectives is a registered
conjecture (`dep/claims.yaml`, `conj.multidim_descent`), not a theorem of this
package.
-/

namespace IGTP

/-- Natural-gradient update step for a scalar parameter `θ`:
`θ' = θ - η · ∇S(θ) / f`, where `f > 0` is the Fisher-metric scalar and
`η > 0` the step size. -/
noncomputable def naturalGradientStep (η f : ℝ) (grad : ℝ → ℝ) (θ : ℝ) : ℝ :=
  θ - η * grad θ / f

/-- One-step strict descent on the quadratic model. For `c > 0`, `f > 0`,
`η > 0` with the step-size condition `η · c ≤ f`, and `θ ≠ 0`, the update
`θ' = θ - η · (c · θ) / f` strictly decreases the objective
`S(θ) = (c/2) · θ²`.

Sharpness of the step-size condition is recorded in `dep/claims.yaml`:
for `η · c > 2 · f` the update strictly increases the objective for `θ ≠ 0`
(see `ex.descent_sharpness`). -/
theorem quadratic_descent_strict {c f η θ : ℝ} (hc : 0 < c) (hf : 0 < f)
    (hη : 0 < η) (hstep : η * c ≤ f) (hθ : θ ≠ 0) :
    (c / 2) * (θ - η * (c * θ) / f) ^ 2 < (c / 2) * θ ^ 2 := by
  have hx : 0 < η * c / f := div_pos (mul_pos hη hc) hf
  have hx2 : η * c / f ≤ 1 := by rwa [div_le_one hf]
  have hprod : (0 : ℝ) ≤ (1 - η * c / f) * (η * c / f) :=
    mul_nonneg (sub_nonneg.mpr hx2) (le_of_lt hx)
  have hsq : (1 - η * c / f) ^ 2 < 1 := by nlinarith [hprod, hx]
  have hθ2 : (0 : ℝ) < θ ^ 2 := by
    rcases lt_or_gt_of_ne hθ with hlt | hgt
    · have h2 : (-θ) ^ 2 = θ ^ 2 := by ring
      rw [← h2]
      exact pow_pos (neg_pos.2 hlt) 2
    · exact pow_pos hgt 2
  have hf0 : f ≠ 0 := ne_of_gt hf
  have expand : (θ - η * (c * θ) / f) ^ 2 = θ ^ 2 * (1 - η * c / f) ^ 2 := by
    field_simp
    ring
  have hkey : (1 - η * c / f) ^ 2 * θ ^ 2 < θ ^ 2 := by
    have h1 := mul_lt_mul_of_pos_right hsq hθ2
    rwa [one_mul] at h1
  rw [expand, mul_comm (θ ^ 2) ((1 - η * c / f) ^ 2)]
  exact mul_lt_mul_of_pos_left hkey (div_pos hc two_pos)

/-- One-step non-strict descent on the quadratic model, with `θ` unrestricted
(including the minimizer `θ = 0`, where equality holds). -/
theorem quadratic_descent_le {c f η θ : ℝ} (hc : 0 < c) (hf : 0 < f)
    (hη : 0 ≤ η) (hstep : η * c ≤ f) :
    (c / 2) * (θ - η * (c * θ) / f) ^ 2 ≤ (c / 2) * θ ^ 2 := by
  have hx : 0 ≤ η * c / f := div_nonneg (mul_nonneg hη (le_of_lt hc)) (le_of_lt hf)
  have hx2 : η * c / f ≤ 1 := by rwa [div_le_one hf]
  have hprod : (0 : ℝ) ≤ (1 - η * c / f) * (η * c / f) :=
    mul_nonneg (sub_nonneg.mpr hx2) hx
  have hsq : (1 - η * c / f) ^ 2 ≤ 1 := by nlinarith [hprod, hx]
  have hθ2 : (0 : ℝ) ≤ θ ^ 2 := sq_nonneg θ
  have hf0 : f ≠ 0 := ne_of_gt hf
  have expand : (θ - η * (c * θ) / f) ^ 2 = θ ^ 2 * (1 - η * c / f) ^ 2 := by
    field_simp
    ring
  have hkey : (1 - η * c / f) ^ 2 * θ ^ 2 ≤ θ ^ 2 := by
    have h1 := mul_le_mul_of_nonneg_right hsq hθ2
    rwa [one_mul] at h1
  rw [expand, mul_comm (θ ^ 2) ((1 - η * c / f) ^ 2)]
  exact mul_le_mul_of_nonneg_left hkey (le_of_lt (div_pos hc two_pos))

/-- The descent theorems transfer to `naturalGradientStep` with the model
gradient `∇S(θ) = c · θ`. -/
theorem naturalGradientStep_descent_strict {c f η θ : ℝ} (hc : 0 < c) (hf : 0 < f)
    (hη : 0 < η) (hstep : η * c ≤ f) (hθ : θ ≠ 0) :
    (c / 2) * (naturalGradientStep η f (fun x => c * x) θ) ^ 2
      < (c / 2) * θ ^ 2 := by
  have h := quadratic_descent_strict hc hf hη hstep hθ
  simpa only [naturalGradientStep] using h

/-- Non-vacuity witness for `quadratic_descent_strict`: the exact rational
instance `c = 1, f = 1, η = 1/2, θ = 1`. -/
example : (1 / 2 : ℝ) * (1 - (1 : ℝ) / 2 * ((1 : ℝ) * 1) / 1) ^ 2
      < (1 / 2) * (1 : ℝ) ^ 2 := by norm_num

end IGTP
