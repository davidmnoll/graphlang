

abbrev Bit := Bool

inductive BSExpr
| const  : ℚ
| incr_at : BSExpr
| decr_at : BSExpr
| add    : BSExpr → BSExpr
-- | mul    : BSExpr → BSExpr → BSExpr
| var    : String → BSExpr
| neg    : BSExpr
-- | inv    : BSExpr → BSExpr                       -- 1 / x
-- | exp    : BSExpr → BSExpr → BSExpr              -- x^y
| concat : BSExpr → BSExpr
-- | I  -- concat ones zeros
| zeros
| ones
-- | real  : ℝ
-- | complex : ℂ


def nsmulBSExpr  : ℕ → BSExpr → BSExpr
| const const
|

instance : Zero BSExpr where
  zero := BSExpr.zeros

instance : AddCommGroup CStream where
  add := BSExpr.add
  zero := BSExpr.zeros
  neg := BSExpr.neg
  nsmul := fun n s => if n % 2 = 0 then 0 else s
  zsmul := fun z s => if z % 2 = 0 then 0 else s





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
--   neg := id
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
