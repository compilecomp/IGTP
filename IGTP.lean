/-
Copyright (c) 2026 the IGTP contributors. Released under the Apache License 2.0.
-/
import IGTP.Manifold
import IGTP.Objective
import IGTP.RicciFlow
import IGTP.QuadraticModel
import IGTP.Boundary

/-!
# IGTP

Information-Geometric Theorem Proving: the formal core of the IGTP framework.

This root module re-exports the five modules of the formal core. All
declarations in this package are proved: the package contains no `sorry`,
no `admit`, no `native_decide`, and no `axiom` declarations. The axiom
ledger (standard Mathlib axioms only) is extracted in CI and archived under
`dep/out/axioms/`.

Design targets that are *not* theorems of this package are registered as
conjectures in `dep/claims.yaml` and are documented with their status in
`doc/DesignGoals.md`.
-/
