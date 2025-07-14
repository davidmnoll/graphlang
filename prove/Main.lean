import Prove.DigitStream


def main : IO Unit := do
  let s := DigitStream.ofFn (fun n => n * n)
  let taken := DigitStream.take 10 s
  IO.println s!"First 10 squares: {taken}"
