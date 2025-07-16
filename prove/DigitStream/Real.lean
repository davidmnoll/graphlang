import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Init.Data.ToString.Basic



def realToString (r : Real) : String := toString r

instance : ToString ℝ where
  toString _ := "ℝ"
