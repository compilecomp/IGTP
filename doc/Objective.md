# Objective

## Abstract

`IGTP.Objective` defines the three objective components of the IGTP action
as explicit nonnegative data and the discrete action functional over a finite
list of times. It takes a `MetricManifold` and nonnegative component
functions; it produces the functional on which the nonnegativity theorem is
stated and proved.

## Formal Definitions

Lean 4 (IGTP/Objective.lean):

```lean
structure ObjectiveComponents (M : Type*) [MetricManifold M] where
  velocity : (γ : ℝ → M) → PathVelocity γ
  smtPotential : (ℝ → M) → ℝ → ℝ
  smt_nonneg : ∀ (γ : ℝ → M) (t : ℝ), 0 ≤ smtPotential γ t
  descriptionLength : (ℝ → M) → ℝ → ℝ
  dl_nonneg : ∀ (γ : ℝ → M) (t : ℝ), 0 ≤ descriptionLength γ t

noncomputable def discreteAction (o : ObjectiveComponents M) (γ : ℝ → M)
    (ts : List ℝ) : ℝ :=
  (ts.map fun t => geodesicEnergy γ (o.velocity γ) t
      + o.smtPotential γ t + o.descriptionLength γ t).sum
```

Component correspondence with the reference engine:

| Lean field | Engine field (bridges/igtp_engine/objective.py) | Role |
|---|---|---|
| `metric p v v` | `EdgeObjective.metric` | metric data |
| `geodesicEnergy` | `DiscreteObjective.energy = (1/2) * metric` | ATP component |
| `smtPotential` | `EdgeObjective.potential` | SMT component |
| `descriptionLength` | `EdgeObjective.description` | ITP component |
| `discreteAction` | `discrete_action(path)` | combined objective |

## Algorithm

The module contains one proved statement, `discreteAction_nonneg`: the
discrete action over a finite time list is nonnegative when the components
are nonnegative. The proof is an induction on the list: the empty list gives
the empty sum, which is 0 by convention (`dep/conventions.yaml`,
`conv.empty_sum`); a cons list adds one nonnegative summand to a nonnegative
remainder. Complexity: the theorem is a proof, not an algorithm; the runtime
analog `discrete_action` runs in O(len(path)) exact-rational operations.

## Invariants

1. `smtPotential γ t ≥ 0` and `descriptionLength γ t ≥ 0` hold for every
   constructed `ObjectiveComponents`; they are discharged at construction
   time as structure fields, not axioms.
2. The discrete action of the empty time list equals 0.
3. `discreteAction_nonneg` depends only on `geodesicEnergy_nonneg` and the
   two nonnegativity fields; the dependency is recorded in `dep/claims.yaml`.

## Integration Points

Depends on: `IGTP.Manifold` (energy and velocity), Mathlib ordered-field
arithmetic. Depended on by: `doc/DesignGoals.md` (the objective is the object
the design goals constrain), the reference engine `objective.py` (runtime
analog). Witnesses: `IGTP.unitObjective` (zero components on the one-point
model).

## Known Limitations

The continuous action functional (an integral over time) is not defined in
this repository; the discrete action over a finite time list is the only
formalized objective, and the continuous minimization statement is registered
as `conj.continuous_geodesic` with status `conjectural`. The K component is a
declared nonnegative proxy; it carries no property connecting it to
Kolmogorov complexity, which is uncomputable. The time list may contain
duplicates and negative times; the theorem holds for both cases, and no
restriction excludes them.
