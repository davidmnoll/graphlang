import Mathlib.Data.Nat.Basic
import Mathlib.Data.Rat.Init
import Mathlib.Data.Int.Basic
import Mathlib.Algebra.Group.Basic

abbrev Bit := Bool

inductive BSExpr
| const  : ℚ -> BSExpr
| nat   : Nat → BSExpr
| incr_at : BSExpr → BSExpr → BSExpr
-- | complex  : ℂ -> BSExpr
-- | add    : BSExpr → BSExpr → BSExpr
-- | mul    : BSExpr → BSExpr → BSExprnst
-- | var    : String → BSExpr
| flipped    : BSExpr -> BSExpr
-- | inv    : BSExpr → BSExpr                       -- 1 / x
-- | exp    : BSExpr → BSExpr → BSExpr              -- x^y
| sum : BSExpr → BSExpr → BSExpr
-- | I  -- concat ones zeros
| zeros
| ones
-- | inf
-- | real  : ℝ
-- | complex : ℂ
deriving Repr



class BitStream (a : Type*) where
  incr: a → BSExpr
  flipped: a → BSExpr
  bit_at: a -> BSExpr -> Option Bool

instance : BitStream BSExpr where
  incr e := match e with
  | .zeros => .ones
  | .ones => .const 1



instance : BitStream Nat where
  incr n := (.const (n + 1))
  flipped n := .const (-(n: Int))
  bit_at n e := match e with
  | .zeros => false
  | .ones => true
  | .flipped e' => not (e.bit_at n e')
  | .nat m => ((n / (2^m)) % 2) = 1
  | .sum e1 e2 => e1.bit_at n e2 || e2.bit_at n e1
  | .incr_at e1 e2 => e1.bit_at n e2 || e2.bit_at n e1
  | .const q =>
    if q >= 0 ∧ q.den = 1 then  -- Check if q is a non-negative integer
      ((n / (2^q)) % 2) = 1
    else
      false



def nsmulBSExpr : ℕ → BSExpr → BSExpr
| 0, _ => .zeros
| _, .zeros => .zeros
| n, .ones => (.const (-(n: ℚ)))
| n, .nat m => if (( n > 0 ) && (m > 0)) then .nat (n * (m: ℕ)) else .zeros
| n, .const q => .const (q * (n: ℚ))
| n, .concat e1 e2 => .concat (nsmulBSExpr n e1) (nsmulBSExpr n e2)
| n, .incr_at e1 e2 => .incr_at (nsmulBSExpr n e1) (nsmulBSExpr n e2)
| n, .flipped e => .flipped (nsmulBSExpr n e)
-- | n, .add e1 e2 => .add (nsmulBSExpr n e1) (nsmulBSExpr n e2)
-- | n, .mul e


def zsmulBSExpr: Int → BSExpr → BSExpr
| 0, _ => .zeros
| _, .zeros => .zeros
| z, .ones => .const (-z)
| z, .nat n => .const (z * (n: Int))
| z, .const q => .const (q * (z: ℚ))
| z, .concat e1 e2 => .concat (zsmulBSExpr z e1) (zsmulBSExpr z e2)
| z, .incr_at e1 e2 => .incr_at (zsmulBSExpr z e1) (zsmulBSExpr z e2)
| z, .flipped e => if z > 0 then (.flipped (zsmulBSExpr z e)) else (zsmulBSExpr (-z) e)
-- | z, .add e1 e2 => .add (zsmulBSExpr z e1) (zsmulBSExpr z e2)
-- | n, .mul e


def add: BSExpr → BSExpr → BSExpr
| .zeros, e => e
| e, .zeros => e
|

instance : Zero BSExpr where
  zero := .zeros

instance : AddCommGroup BSExpr where
  add := .add
  zero := .zeros
  flipped := .flipped
  nsmul := nsmulBSExpr
  zsmul := zsmulBSExpr





-- def fracToBinaryStream (x : ℝ) : Stream Bit :=
--   corec (fun x =>
--     let y := 2 * x
--     if y ≥ 1 then (true, y - 1) else (false, y)
--   ) x

-- def RStream := ℝ → Bit

-- def addRStream (a b : RStream) : RStream := fun r =>
--   sum = a + b
--   frac = r - Real.floor r


--   if r < 0 then



-- def zeroRStream : RStream := fun _ => false

-- instance : Zero RStream where
--   zero := zeroRStream

-- def getRStream :=




-- def zeroCStream : CStream := fun _ => false

-- instance : Zero CStream where
--   zero := zeroCStream


-- instance : Add CStream where
--   add := addCStream

-- instance : AddCommGroup CStream where
--   add := (· + ·)
--   zero := 0
--   flipped := id
--   nsmul := fun n s => if n % 2 = 0 then 0 else s
--   zsmul := fun z s => if z % 2 = 0 then 0 else s


-- instance : Mul CStream where
--   mul := CStream.mulNoCarry  -- or your carry-aware mul

-- def oneCStream : CStream :=
--   {
--     get := fun z => if z = { re := 0, im := 0 } then true else false
--   }

-- instance : One CStream where
--   one := oneCStream

-- instance : Pow CStream Nat where
--   pow := powHelper

-- def getCStream : ℂ → CStream := fun (re, im) =>
--   let front RealBitStrWithBody BitBody.ones := {
--     head := [],
--     body := BitBody.ones
--     tail := []
--   }
--   let back RealBitStrWithBody BitBody.zeros := {

--   }
--   let ComplexBitStr










-- structure RealBitStr where :=
--   head : List Bit
--   body   : BitBody
--   tail : List Bit
--   deriving Repr


-- structure RealBitStrWithBody (b : BitBody) where
--   val : RealBitStr
--   body_eq : val.body = b

-- structure ComplexBitStr where :=
--   front: RealBitStrWithBody BitBody.ones
--   back: RealBitStrWithBody BitBody.zeros

-- structure ComplexBitStrSum where :=
--   operand: List ComplexBitStr

-- structure ComplexBitStrProd where :=
--   entries: List ComplexBitStr

-- structure ComplexBitStrExp where :=
--   entry: List ComplexBitStr
