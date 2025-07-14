import Lake
open Lake DSL

package prove

require batteries from git
  "https://github.com/leanprover-community/batteries" @ "main"

@[default_target]
lean_lib Prove

lean_exe prove where
  root := `Main
