import DigitStream.Basic




def main : IO Unit := do
  -- let example1 : ℂ := 1 + 2 * Complex.I
  let example1 : BitStr := [1, 1] zeros []
  let example2 : BitStr := [] ones []

  let sum : BitStr := example1 + example2

  IO.println s!"sum: {sum}"
