# Results table (generated; never hand-edited)

| ID | Node | Statement | Claim status | Complete? | Depends on | Witness | Gap |
|---|---|---|---|---|---|---|---|
| res.energy_nonneg | IGTP.geodesicEnergy_nonneg | "For every path γ and velocity assignment v, the geodesic energy density E(γ, v, t) = (1/2) g_{γ(t)}(v(t), v(t)) is nonnegative." | machine-checked | complete | - | IGTP.instMetricManifoldUnit | none |
| res.action_nonneg | IGTP.discreteAction_nonneg | "The discrete action S(γ, ts), the sum over a finite time list of E + V + K, is nonnegative whenever V and K are nonnegative componentwise." | machine-checked | complete | res.energy_nonneg | IGTP.unitObjective | none |
| res.ricci_const | IGTP.isRicciFlow_const | "A time-constant metric family satisfies the Ricci-flow equation ∂_t g = -2 R if and only if the declared Ricci data vanishes identically." | machine-checked | complete | - | "zero family on Unit (example after isRicciFlow_const in IGTP/RicciFlow.lean)" | none |
| res.descent_strict | IGTP.quadratic_descent_strict | "For c > 0, f > 0, η > 0 with η c ≤ f, and θ ≠ 0, the natural-gradient update θ' = θ - η (c θ)/f strictly decreases the quadratic objective S(θ) = (c/2) θ²." | machine-checked | complete | - | "exact rational instance c = 1, f = 1, η = 1/2, θ = 1 (example in IGTP/QuadraticModel.lean)" | none |
| res.descent_le | IGTP.quadratic_descent_le | "For c > 0, f > 0, η ≥ 0 with η c ≤ f, the update never increases the quadratic objective, for every θ." | machine-checked | complete | - | "θ = 0 instance: equality holds (battery dg.quadratic_descent_le.zero)" | none |
| res.descent_step | IGTP.naturalGradientStep_descent_strict | "The strict descent theorem transfers to the IGTP.naturalGradientStep update with the model gradient ∇S(θ) = c θ." | machine-checked | complete | res.descent_strict | "battery probe dg.natural_gradient.step_def" | none |
| res.anchors_exist | IGTP.exists_path_satisfies_anchors | "Every consistent, nonempty-universe anchor set is satisfied by some path." | machine-checked | complete | - | "singleton anchor set witness (example in IGTP/Boundary.lean); battery dg.anchors" | none |
| res.anchor_congr | IGTP.satisfiesAnchor_congr | "Anchor satisfaction is invariant under replacing a path by one agreeing with it at the anchor time." | machine-checked | complete | - | "battery dg.congr.00" | none |
| conj.continuous_geodesic | - | "On a smooth realization of the IGTP manifold, minimizers of a continuous action functional built from E + V + K follow geodesics of the semantic metric." | conjectural | placeholder | - | - | none |
| conj.search_complexity | - | "Search cost on the smoothed manifold is polynomial in the size of the problem instance." | conjectural | placeholder | - | - | none |
| conj.kolmogorov_minimality | - | "Among searched candidate paths, minimizing the action selects a proof path of minimal algorithmic complexity." | conjectural | placeholder | - | - | none |
| conj.ricci_pruning | - | "Ricci-flow preprocessing reduces the explored search space relative to unsmoothed syntactic search." | conjectural | placeholder | - | - | none |
| conj.multidim_descent | - | "One-step natural-gradient descent decreases the objective in multidimensional state spaces under Lipschitz and convexity conditions relative to the Fisher m... | conjectural | placeholder | - | - | none |
| conj.curvature_discovery | - | "Curvature defects of the manifold indicate locations where theorems are missing (structure-guided conjecture generation)." | conjectural | placeholder | - | - | none |
| emp.resolution_engine | - | "The propositional resolution engine decides entailment on the test battery, and every produced derivation passes the clause-level soundness criterion." | empirical | complete | - | - | none |
| emp.smt_crosscheck | - | "z3 at the pinned version agrees with the resolution engine on every task of the reference pipeline." | empirical | complete | - | - | none |
| emp.search_energy | - | "Geodesic search returns the minimum combined-energy path on the demo manifold, matching hand-computed exact optima." | empirical | complete | - | - | none |
