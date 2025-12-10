


inductive GLNode where
  | empty : GLNode
  | mk: GLNode -> GLNode -> GLNode -> GLNode
  deriving DecidableEq, Repr


def zero : GLNode := GLNode.empty

def one : GLNode := GLNode.mk zero zero zero



/--
Goal: prove that GLNode has an isomorphism to Nat
-/

def of_int  : Nat -> GLNode
  | 0 => zero
  | n+1 => GLNode.mk (of_int n) zero zero
