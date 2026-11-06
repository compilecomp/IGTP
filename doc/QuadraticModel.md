# QuadraticModel

## Abstract

`IGTP.QuadraticModel` defines the natural-gradient update step for a scalar
parameter and proves one-step descent for the quadratic objective
S(θ) = (c/2)·θ² under an explicit step-size condition. It takes positive
reals c, f, a step size η, and a parameter θ; it produces the update
definition and two descent theorems (strict and non-strict).

## Formal Definitions

Lean 4 (IGTP/QuadraticModel.lean):

```lean
noncomputable def naturalGradientStep (η f : ℝ) (grad : ℝ → ℝ) (θ : ℝ) : ℝ :=
  θ - η * grad θ / f

theorem quadratic_descent_strict {c f η θ : ℝ} (hc : 0 < c) (hf : 0 < f)
    (hη : 0 < η) (hstep : η * c ≤ f) (hθ : θ ≠ 0) :
    (c / 2) * (θ - η * (c * θ) / f) ^ 2 < (c / 2) * θ ^ 2

theorem quadratic_descent_le {c f η θ : ℝ} (hc : 0 < c) (hf : 0 < f)
    (hη : 0 ≤ η) (hstep : η * c ≤ f) :
    (c / 2) * (θ - η * (c * θ) / f) ^ 2 ≤ (c / 2) * θ ^ 2
```

`f` is the Fisher-metric scalar, `η` the step size, `c` the curvature of the
quadratic model. The update with model gradient ∇S(θ) = c·θ is
`naturalGradientStep η f (fun x => c * x) θ`.

## Algorithm

The strict proof: with x = η·c/f, the hypotheses give 0 < x ≤ 1. The identity
(θ - η(cθ)/f)² = θ²(1 - x)² is established by `field_simp` and `ring`. The
factor (1 - x)² is strictly below 1 for 0 < x ≤ 1, proved by `nlinarith` from
the explicit product (1 - x)·x ≥ 0; multiplication by θ² > 0 and then by
c/2 > 0 gives the strict inequality. The non-strict proof follows the same
steps with ≤ throughout and θ unrestricted. Complexity: closed-form real
algebra; no computation, no search. Degenerate cases are covered: θ = 0 gives
equality (non-strict theorem) and is the sharpness witness for the strict
hypothesis H5.

## Invariants

1. All five hypotheses of the strict theorem are explicit binders; none is
   inherited from context.
2. The step-size condition is sharp: for η·c > 2·f the update strictly
   increases the objective for θ ≠ 0 (battery probe
   `dg.quadratic_descent_strict.sharp`, exact arithmetic).
3. Every descent claim in the repository is either one of these two theorems
   or registered as `conj.multidim_descent`; no other descent is asserted.

## Integration Points

Depends on: Mathlib ordered-field arithmetic and `nlinarith`. Depended on by:
`doc/DesignGoals.md` (Goal 1 and Goal 2 status discussion); no Lean module
imports this one yet. The runtime analog of the update is part of the search
loop of `GeodesicSearch` only conceptually; the engine implements discrete
Dijkstra search, not gradient descent, and no claim links the two beyond the
status records in `dep/claims.yaml`.

## Known Limitations

The theorems cover the one-dimensional quadratic model only. The
multidimensional and non-quadratic cases are `conj.multidim_descent`, status
`conjectural`; no Lipschitz or convexity framework exists in this repository.
The update is defined with real division and is `noncomputable`; no
floating-point implementation exists, and none is claimed. The Fisher metric
is a positive scalar here; the matrix-valued case is future work.
