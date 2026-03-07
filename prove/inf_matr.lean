structure DigitDigitStream (α : Type) where
  head : α
  tail : Thunk (DigitStream α)

namespace DigitStream

-- Helper to get the tail DigitStream
def tail (s : DigitDigitStream α) : DigitStream α := s.tail.get

-- Map function over DigitStream
def map {α β : Type} (f : α → β) (s : DigitStream α) : DigitStream β :=
  { head := f s.head,
    tail := Thunk.mk (map f s.tail.get) }

-- Zip two DigitStreams with a function
def zipWith {α β γ : Type} (f : α → β → γ) (s1 : DigitStream α) (s2 : DigitStream β) : DigitStream γ :=
  { head := f s1.head s2.head,
    tail := Thunk.mk (zipWith f s1.tail.get s2.tail.get) }

end DigitStream

-- Base for digits (example: base 10)
def base : Int := 10

open DigitStream

-- Add two digit DigitStreams with carry propagation
partial def addWithCarry : DigitStream Int → DigitStream Int → Int → DigitStream Int
  | s1, s2, carryIn =>
    let sum := s1.head + s2.head + carryIn
    let digit := sum % base
    let carryOut := sum / base
    { head := digit,
      tail := Thunk.mk (addWithCarry s1.tail.get s2.tail.get carryOut) }

-- Example: DigitStream of zeros
def zeros : DigitStream Int :=
  { head := 0,
    tail := Thunk.mk zeros }

-- Example: DigitStream of ones
def ones : DigitStream Int :=
  { head := 1,
    tail := Thunk.mk ones }

-- Convert Nat to digit DigitStream (in base `base`), infinite DigitStream with zeros after finite digits
partial def natToDigitStream (n : Nat) : DigitStream Int :=
  let digit := (n % (base.toNat))
  let rest := n / (base.toNat)
  { head := digit,
    tail := Thunk.mk (if rest = 0 then zeros else natToDigitStream rest) }

-- Take first n digits from a DigitStream and collect as list (for printing)
def take (n : Nat) : DigitStream α → List α
  | 0, _ => []
  | n+1, s => s.head :: take n s.tail.get

-- Example usage
def main : IO Unit := do
  let a := natToDigitStream 1234
  let b := natToDigitStream 5678
  let sum := addWithCarry a b 0
  let digits := take 10 sum
  IO.println s!"Sum digits (base {base}): {digits}"
