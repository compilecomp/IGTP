/-
Copyright (c) 2026 the IGTP contributors. Released under the Apache License 2.0.
-/
import IGTP.Manifold

/-!
# IGTP.Objective

The objective components of the IGTP action, as explicit nonnegative data, and
the discrete action functional over a finite list of times.

The three components are: geodesic energy (ATP component), a constraint
potential (SMT component), and a description-length regularizer (ITP component).
Nonnegativity of the two parameterized components is stated as structure fields,
not as axioms; a concrete `ObjectiveComponents` must discharge them at
construction time.
-/

namespace IGTP

variable {M : Type*} [MetricManifold M]

/-- The three objective components of the IGTP action, as explicit data.

* `velocity` is the velocity assignment used by the geodesic-energy term.
* `smtPotential V(γ, t)` penalizes paths violating arithmetic or boolean
  constraints; it is the SMT component.
* `descriptionLength K(γ, t)` penalizes proof steps of high algorithmic
  complexity; it is the ITP component and a declared proxy for Kolmogorov
  complexity, which is uncomputable (see `doc/Objective.md`, Known Limitations).

The nonnegativity fields are hypotheses discharged at construction, not axioms. -/
structure ObjectiveComponents (M : Type*) [MetricManifold M] where
  /-- Velocity assignment along each path. -/
  velocity : (γ : ℝ → M) → PathVelocity γ
  /-- The constraint potential `V(γ, t)`. -/
  smtPotential : (ℝ → M) → ℝ → ℝ
  /-- Discharged nonnegativity of `smtPotential`. -/
  smt_nonneg : ∀ (γ : ℝ → M) (t : ℝ), 0 ≤ smtPotential γ t
  /-- The description-length regularizer `K(γ, t)`. -/
  descriptionLength : (ℝ → M) → ℝ → ℝ
  /-- Discharged nonnegativity of `descriptionLength`. -/
  dl_nonneg : ∀ (γ : ℝ → M) (t : ℝ), 0 ≤ descriptionLength γ t

/-- The discrete action of a path over a finite list of times `ts`:
the sum over `ts` of `E + V + K` in the given order of summands.

This is the load-bearing discrete analog of the continuous action functional;
the continuous statement is a registered conjecture, not a theorem of this
package (see `dep/claims.yaml`, `conj.continuous_geodesic`). -/
noncomputable def discreteAction (o : ObjectiveComponents M) (γ : ℝ → M) (ts : List ℝ) : ℝ :=
  (ts.map fun t =>
    geodesicEnergy γ (o.velocity γ) t + o.smtPotential γ t
      + o.descriptionLength γ t).sum

/-- The discrete action is nonnegative. Hypotheses used: `smt_nonneg`,
`dl_nonneg`, and `geodesicEnergy_nonneg`. -/
theorem discreteAction_nonneg (o : ObjectiveComponents M) (γ : ℝ → M) (ts : List ℝ) :
    0 ≤ discreteAction o γ ts := by
  induction ts with
  | nil =>
      simp only [discreteAction, List.map_nil, List.sum_nil]
      exact le_refl _
  | cons t ts ih =>
      simp only [discreteAction, List.map_cons, List.sum_cons]
      exact add_nonneg
        (add_nonneg
          (add_nonneg (geodesicEnergy_nonneg γ (o.velocity γ) t) (o.smt_nonneg γ t))
          (o.dl_nonneg γ t))
        ih

/-- Non-vacuity witness for `ObjectiveComponents` and `discreteAction_nonneg`:
the zero objective on the one-point model (`IGTP.instMetricManifoldUnit`). -/
def unitObjective : ObjectiveComponents Unit where
  velocity := fun _ _ => (0 : ℝ)
  smtPotential := fun _ _ => 0
  smt_nonneg := fun _ _ => le_refl 0
  descriptionLength := fun _ _ => 0
  dl_nonneg := fun _ _ => le_refl 0

/-- Instantiation of `unitObjective`: the zero objective has zero discrete
action over the empty time list (the empty-sum convention). -/
example : discreteAction unitObjective (fun _ => ()) [] = 0 := by
  simp only [discreteAction, List.map_nil, List.sum_nil]

/-- Instantiation of `unitObjective` at a nonempty time list: the action
equals the energy sum of the zero components, which is 0 at the zero
velocities. -/
example : discreteAction unitObjective (fun _ => ()) [3, 7] = 0 := by
  simp only [discreteAction, List.map_cons, List.sum_cons, geodesicEnergy,
    unitObjective, instMetricManifoldUnit]
  norm_num

end IGTP
