/-
Copyright (c) 2026 the IGTP contributors. Released under the Apache License 2.0.
-/
import Mathlib

/-!
# IGTP.Boundary

Dirichlet-style anchors for human-machine collaboration: a set of `(time, point)`
constraints on a path, the consistency condition, and the existence theorem for
paths satisfying a consistent anchor set.

This models the ITP interaction mode of IGTP: the human fixes boundary values
(the anchor points), and the machine interpolates a proof path between them.
Only the anchor constraints are formalized here; the interpolation objective is
the subject of `IGTP.Objective`.
-/

namespace IGTP

/-- The anchor condition for a path `γ` and an anchor `a = (t, p)`:
`γ` takes the value `p` at time `t`. -/
def SatisfiesAnchor {M : Type*} (γ : ℝ → M) (a : ℝ × M) : Prop := γ a.1 = a.2

/-- A set of Dirichlet anchors on paths `ℝ → M`. -/
abbrev AnchorSet (M : Type*) := Set (ℝ × M)

/-- Consistency of an anchor set: no two distinct points are anchored at the
same time. -/
def AnchorConsistent {M : Type*} (A : AnchorSet M) : Prop :=
  ∀ (t : ℝ) (p q : M), (t, p) ∈ A → (t, q) ∈ A → p = q

/-- Every consistent anchor set is satisfied by some path. The construction
selects, for each time, the (classically chosen) witness anchored there, or an
arbitrary point when no anchor exists; consistency makes the selection
well defined. Classical choice is used and is recorded in the axiom ledger. -/
theorem exists_path_satisfies_anchors {M : Type*} [Nonempty M]
    (A : AnchorSet M) (hcons : AnchorConsistent A) :
    ∃ γ : ℝ → M, ∀ a ∈ A, SatisfiesAnchor γ a := by
  open scoped Classical in
  refine ⟨fun t => if h : ∃ p, (t, p) ∈ A then h.choose else Classical.arbitrary M, ?_⟩
  intro a ha
  have hx : ∃ p, (a.1, p) ∈ A := ⟨a.2, ha⟩
  show (if h : ∃ p, (a.1, p) ∈ A then h.choose else Classical.arbitrary M) = a.2
  rw [dif_pos hx]
  exact hcons a.1 hx.choose a.2 hx.choose_spec ha

/-- Non-vacuity witness for `exists_path_satisfies_anchors`: a singleton anchor
set is consistent and satisfied by the constant path at its point. -/
example {M : Type*} [Nonempty M] (t₀ : ℝ) (p₀ : M) :
    ∃ γ : ℝ → M, ∀ a ∈ ({(t₀, p₀)} : AnchorSet M), SatisfiesAnchor γ a := by
  have hcons : AnchorConsistent ({(t₀, p₀)} : AnchorSet M) := by
    intro t p q hp hq
    have hp' : p = p₀ :=
      congrArg Prod.snd (show (t, p) = (t₀, p₀) from Set.mem_singleton_iff.mp hp)
    have hq' : q = p₀ :=
      congrArg Prod.snd (show (t, q) = (t₀, p₀) from Set.mem_singleton_iff.mp hq)
    rw [hp', hq']
  exact exists_path_satisfies_anchors _ hcons

/-- Anchor conditions are invariant under replacing a path by one that agrees
with it at the anchor time. -/
theorem satisfiesAnchor_congr {M : Type*} {γ σ : ℝ → M} {a : ℝ × M}
    (h : σ a.1 = γ a.1) (hγ : SatisfiesAnchor γ a) : SatisfiesAnchor σ a := by
  show σ a.1 = a.2
  rw [h, hγ]

end IGTP
