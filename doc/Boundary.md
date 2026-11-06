# Boundary

## Abstract

`IGTP.Boundary` defines Dirichlet-style anchors on paths, the consistency
condition on an anchor set, the existence theorem for paths satisfying a
consistent anchor set, and the invariance of anchor satisfaction under path
replacement. It takes a set of (time, point) pairs; it produces the anchor
predicates and two proved theorems.

## Formal Definitions

Lean 4 (IGTP/Boundary.lean):

```lean
def SatisfiesAnchor {M : Type*} (γ : ℝ → M) (a : ℝ × M) : Prop := γ a.1 = a.2

abbrev AnchorSet (M : Type*) := Set (ℝ × M)

def AnchorConsistent {M : Type*} (A : AnchorSet M) : Prop :=
  ∀ (t : ℝ) (p q : M), (t, p) ∈ A → (t, q) ∈ A → p = q

theorem exists_path_satisfies_anchors {M : Type*} [Nonempty M]
    (A : AnchorSet M) (hcons : AnchorConsistent A) :
    ∃ γ : ℝ → M, ∀ a ∈ A, SatisfiesAnchor γ a

theorem satisfiesAnchor_congr {M : Type*} {γ σ : ℝ → M} {a : ℝ × M}
    (h : σ a.1 = γ a.1) (hγ : SatisfiesAnchor γ a) : SatisfiesAnchor σ a
```

## Algorithm

The existence proof constructs the path: at each time t, if some point is
anchored at t, the path takes the classically chosen witness; otherwise it
takes an arbitrary point of the nonempty universe. Consistency makes the
selection well defined: two anchors at one time carry the same point. The
construction uses classical choice (`Classical.choose` via the
`∃`-witness of the `dite` and `Classical.arbitrary`), which is recorded in
the axiom ledger. The congruence proof rewrites the agreement hypothesis and
applies the anchor condition of the base path. Complexity: the construction
is a function definition; no search is involved.

## Invariants

1. Consistency is exactly the condition under which the constructed path is
   well defined; the theorem fails without it (battery probes
   `dg.anchors.04`, `dg.anchors.06`: conflicting anchor sets).
2. The existential follows the universal: the path is constructed after the
   anchor set is fixed; the quantifier prefix is A A E
   (`dep/fidelity/res.anchors_exist.yaml`).
3. Classical choice appears only through the two named constructions and is
   ledgered in `dep/axioms.yaml` with its strength classification.

## Integration Points

Depends on: Mathlib set membership and classical choice. Depended on by: no
module imports this one yet; the human-machine interaction stage of
`doc/DesignGoals.md` (Goal 3) is its consumer. Witnesses: the singleton
anchor set example in the module and battery `dg.anchors`.

## Known Limitations

The module fixes anchor values only; it does not define the interpolation
objective between anchors, does not construct a least-action path through
them, and does not connect anchors to the objective components of
`IGTP.Objective`. The interpolation is future work. The anchor set may be
infinite; the proof covers that case through classical choice, and no
constructive variant is provided. The theorem requires a nonempty universe;
the empty universe is excluded by hypothesis H2, whose sharpness is recorded
in `dep/hypotheses.yaml`.
