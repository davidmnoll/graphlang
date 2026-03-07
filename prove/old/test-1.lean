import Init.Data.Nat.Basic
import Init.Data.Int.Basic
import Std.Data.List.Basic
open Std

/-- Our custom lazy stream type -/
structure DigitStream (α : Type) where
  head : α
  tail : Thunk (DigitStream α)

namespace DigitStream

-- Tail getter
def tail (s : DigitStream α) : DigitStream α := s.tail.get

-- Map over DigitStream
def map {α β} (f : α → β) : DigitStream α → DigitStream β
  | ⟨h, t⟩ => ⟨f h, Thunk.mk (map f t.get)⟩

-- Zip two streams
def zipWith {α β γ} (f : α → β → γ) : DigitStream α → DigitStream β → DigitStream γ
  | ⟨h1, t1⟩, ⟨h2, t2⟩ =>
    ⟨f h1 h2, Thunk.mk (zipWith f t1.get t2.get)⟩

-- Take first n elements
def take : Nat → DigitStream α → List α
  | 0, _ => []
  | n+1, s => s.head :: take n s.tail.get

-- Create a stream from a function
partial def ofFn (f : Nat → α) (n := 0) : DigitStream α :=
  ⟨f n, Thunk.mk (ofFn f (n+1))⟩

-- Convert to Nat → α stream
partial def toIndexed (s : DigitStream α) : Nat → α :=
  fun n =>
    match n with
    | 0 => s.head
    | n'+1 => toIndexed s.tail.get n'

end DigitStream

/-- Built-in Stream is just `Nat → α` -/
abbrev LeanStream (α : Type) := Nat → α

namespace LeanStream

-- Map over Lean stream
def map {α β} (f : α → β) (s : LeanStream α) : LeanStream β :=
  fun n => f (s n)

-- Zip two Lean streams
def zipWith {α β γ} (f : α → β → γ) (s₁ s₂ : LeanStream α) : LeanStream γ :=
  fun n => f (s₁ n) (s₂ n)

-- Convert to DigitStream
partial def toDigitStream {α} (f : Nat → α) (n := 0) : DigitStream α :=
  ⟨f n, Thunk.mk (toDigitStream f (n+1))⟩

end LeanStream

/-- Test and compare both stream types -/
def main : IO Unit := do
  -- Custom DigitStream of natural numbers
  let s1 := DigitStream.ofFn (fun n => n)
  let takeS1 := DigitStream.take 10 s1

  -- Built-in Lean Stream of natural numbers
  let s2 : LeanStream Nat := fun n => n
  let s2ds := LeanStream.toDigitStream s2
  let takeS2 := DigitStream.take 10 s2ds

  -- Map test
  let mapped1 := DigitStream.map (· + 10) s1
  let mapped2 := LeanStream.map (· + 10) s2
  let takeM1 := DigitStream.take 10 mapped1
  let takeM2 := DigitStream.take 10 (LeanStream.toDigitStream mapped2)

  IO.println "DigitStream.ofFn (n ↦ n) → first 10 elements:"
  IO.println takeS1

  IO.println "LeanStream (n ↦ n) converted to DigitStream → first 10 elements:"
  IO.println takeS2

  IO.println "DigitStream mapped (n ↦ n + 10):"
  IO.println takeM1

  IO.println "LeanStream mapped (n ↦ n + 10), converted to DigitStream:"
  IO.println takeM2
