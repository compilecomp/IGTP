import Lake
open Lake DSL

package «IGTP» where
  version := v!"0.1.0"

@[default_target]
lean_lib «IGTP» where

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "4bbdccd9c5f862bf90ff12f0a9e2c8be032b9a84"
