import Mathlib.Data.Complex.Basic
import Mathlib.Data.Stream.Basic
import Std.Data.List.Basic



inductive BitBody
  | zeros   -- ∞ stream of 0s
  | ones    -- ∞ stream of 1s
  | stream (s : Stream Bit)
  deriving Repr



def CStream := ℂ → Bit

def getCStream : ℂ → CStream := fun (re, im) =>
  let front RealBitStrWithBody BitBody.ones := {
    head := [],
    body := BitBody.ones
    tail := []
  }
  let ComplexBitStr


structure ComplexBitStrSum where :=
  operand: List ComplexBitStr

structure ComplexBitStrProd where :=
  entries: List ComplexBitStr

structure ComplexBitStrExp where :=
  entry: List ComplexBitStr


def zeroCStream : CStream := fun _ => false

instance : Zero CStream where
  zero := zeroCStream


instance : Add CStream where
  add := addCStream

instance : AddCommGroup CStream where
  add := (· + ·)
  zero := 0
  neg := id
  nsmul := fun n s => if n % 2 = 0 then 0 else s
  zsmul := fun z s => if z % 2 = 0 then 0 else s

instance : Mul CStream where
  mul := CStream.mulNoCarry  -- or your carry-aware mul

def oneCStream : CStream :=
  {
    get := fun z => if z = { re := 0, im := 0 } then true else false
  }

instance : One CStream where
  one := oneCStream

instance : Pow CStream Nat where
  pow := powHelper



def addCStream (a b : CStream) : CStream :=


abbrev Bit := Bool

structure RealBitStr where :=
  head : List Bit
  body   : BitBody
  tail : List Bit
  deriving Repr


structure RealBitStrWithBody (b : BitBody) where
  val : RealBitStr
  body_eq : val.body = b

structure ComplexBitStr where :=
  front: RealBitStrWithBody BitBody.ones
  back: RealBitStrWithBody BitBody.zeros
