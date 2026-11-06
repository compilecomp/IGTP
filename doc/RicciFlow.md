# RicciFlow

## Abstract

`IGTP.RicciFlow` defines the Ricci-flow equation for a time-dependent family
of metric component functions on a `MetricManifold` and proves that a
time-constant family is a Ricci flow exactly when the declared Ricci data
vanishes. It takes a metric component family; it produces the flow predicate
and the characterization theorem.

## Formal Definitions

Lean 4 (IGTP/RicciFlow.lean):

```lean
def MetricFamily (M : Type*) [_inst : MetricManifold M] : Type _ :=
  ℝ → ∀ p : M, Tangent p → Tangent p → ℝ

def IsRicciFlowAt (g : MetricFamily M) (t : ℝ) (p : M) (u v : Tangent p) : Prop :=
  deriv (fun s : ℝ => g s p u v) t = -2 * ricci p u v

def IsRicciFlow (g : MetricFamily M) : Prop :=
  ∀ (t : ℝ) (p : M) (u v : Tangent p), IsRicciFlowAt g t p u v
```

Theorem (`res.ricci_const` in `dep/claims.yaml`):

```lean
theorem isRicciFlow_const (g : ∀ p : M, Tangent p → Tangent p → ℝ) :
    IsRicciFlow (fun _ p => g p) ↔ ∀ (p : M) (u v : Tangent p), ricci p u v = 0
```

## Algorithm

The proof of the forward direction applies `deriv_const`: the time derivative
of a constant component is 0, so the flow equation forces `-2 · R = 0`, and
`linarith` extracts `R = 0`. The backward direction substitutes the vanishing
Ricci data into the flow equation and applies `deriv_const` again. The
derivative is the classical derivative of Mathlib
(`Mathlib.Analysis.Calculus.Deriv.Basic`); no weak or distributional
derivative is involved, and no interchange of limits occurs.

## Invariants

1. The flow equation is pointwise in `(t, p, u, v)`; no integrability or
   regularity condition beyond the existence of the derivative in `s` is
   used.
2. Both directions of the iff are kernel-checked; the axiom ledger is the
   standard Mathlib set (`dep/out/axioms/IGTP.isRicciFlow_const.json`).
3. The non-vacuity witness (the zero family on the one-point model) is an
   example in the same module.

## Integration Points

Depends on: `IGTP.Manifold` (tangent family and Ricci data),
`Mathlib.Analysis.Calculus.Deriv.Basic`. Depended on by: no module imports
this one yet; the smoothing stage of the target end state
(`doc/DesignGoals.md`) is its consumer. The smoothing-to-search connection is
`conj.ricci_pruning`, status `conjectural`.

## Known Limitations

`ricci` is declared data of `MetricManifold`; the theorem characterizes flow
families against this data, not against a Ricci tensor derived from
`metric`. Deriving the Ricci tensor from the metric (and the statement that
the flow of a smooth metric exists) is future work and is not claimed
anywhere in this repository. The definition quantifies over all times and
tangent vectors; no short-time existence, uniqueness, or singularity
statement exists here. The search-space consequence of smoothing is not
implemented; `doc/DesignGoals.md`, Goal 1, records the status.
