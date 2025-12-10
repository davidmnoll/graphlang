import Mathlib.Data.Complex.Basic



structure DigitWreath where
  op   : Thunk DigitWreathPoint
  left : Thunk DigitWreathPoint
  right : Thunk DigitWreathPoint


structure DigitStream where
  head: Bool
  tail: Option (Thunk DigitStream)


def dummyStream : DigitStream :=
{ head := false,
  tail := Option.none
}

instance : Inhabited DigitStream :=
⟨dummyStream⟩


/--
Arg1: Base DigitWreath => the number you're trying to get the digits of
Arg2: The Starting index

Return: A structure with head and the ability to get the next digit
-/
def DigitWreath.digit : DigitWreath → DigitWreath → Bool
| t, u => sorry


def DigitWreath.incr : DigitWreath -> DigitWreath
| t => sorry


def DigitWreath.compose : DigitWreath -> DigitWreath
| t => sorry


/--
Arg1: Base DigitWreath => the number you're trying to get the digits of
Arg2: The Starting index

Return: A structure with head and the ability to get the next digit
-/

partial def DigitWreath.digits : DigitWreath -> DigitWreath -> DigitStream
| t, u => {
    head := DigitWreath.digit t u,
    tail:= Option.some ( Thunk.mk (fun _ => DigitWreath.digits t (DigitWreath.incr u)) )
  }


#check Complex


def DigitWreath.from_int: Int -> DigitWreath := sorry
def DigitWreath.from_complex: Complex -> DigitWreath := sorry
