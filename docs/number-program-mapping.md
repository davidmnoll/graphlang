# Mapping Numbers to Programs: Design Alternatives

This document explores different schemes for mapping integers to hypergraph programs, where each graph is identified by a content-addressed integer derived from its structure.

## Core Model

A **graph** (or term/expression) is a set of (left, right) pairs, where each left and right entry is itself a graph identified by its integer address.

```
Graph = Set of (GraphId, GraphId)
GraphId = Integer (content address)
```

The empty graph has ID 0.

---

## Approach 1: Space-Filling Curve Encoding

### Mechanism

1. Treat (left, right) pairs as matrix coordinates
2. Set `matrix[left][right] = 1` for each pair
3. Use Hilbert curve to linearize the matrix into a bit string
4. Reverse the bit string
5. Convert to decimal → this is the graph's ID

### Example

Graph with edges `{(0,0), (0,1), (1,1)}`:
```
Matrix:     Hilbert traversal:    Bit string: 1011
  0 1                             Reversed:   1011
0 [1 1]     Position 0 → (0,0)    Decimal:    11
1 [0 1]     Position 1 → (0,1)
            Position 2 → (1,0)
            Position 3 → (1,1)
```

### Properties

- **Bijective**: Every integer maps to exactly one graph structure
- **Content-addressed**: Same structure always produces same ID
- **No semantic meaning**: Coordinates (i,j) have no inherent interpretation

### Natural Numbers in This Scheme

```
nat(0) = 0                    (empty graph)
nat(1) = {(0, 0)}             → some integer k₁
nat(2) = {(0, k₁)}            → some integer k₂
nat(n) = {(0, nat(n-1))}      → computed recursively
```

The "left = 0" convention marks these as natural number constructors.

---

## Approach 2: Semantic Coordinate Regions

### Core Idea

Assign semantic meaning to different regions of the matrix:

```
        j (right)
        0   1   2   3   ...
      ┌───┬───┬───┬───┬───
    0 │ ? │ + │ + │ + │ ...   (0, n): POSITIVE / Constructor
  i   ├───┼───┼───┼───┼───
(left)│ - │ D │   │   │       (n, 0): NEGATIVE / Destructor
    1 │   │   │   │   │       (n, n): DATA constructors
      ├───┼───┼───┼───┼───
    2 │ - │   │ D │   │       (n, m) where n≠m, n≠0, m≠0: ???
      ├───┼───┼───┼───┼───
    3 │ - │   │   │ D │
      └───┴───┴───┴───┴───
```

### Region Semantics

#### (0, n) — Positive/Constructor Region
- **Role**: Build structure, iterate, produce
- `(0, 1)` = successor / increment
- `(0, n)` = "apply constructor n times" or "produce n units"
- Repeated iteration creates larger structures

#### (n, 0) — Negative/Destructor Region
- **Role**: Consume structure, pattern match, destruct
- `(1, 0)` = predecessor / decrement (consume one unit)
- `(n, 0)` = "consume n units" or "match and discard n-deep structure"
- Pattern matching that throws away matched structure

#### (n, n) — Diagonal / Data Constructors
- **Role**: Tagged data, type markers
- `(1, 1)` = first data constructor (like `True` or `Cons`)
- `(2, 2)` = second data constructor (like `False` or `Nil`)
- Distinguished from operations by being "balanced"

#### (n, m) where n ≠ m, n ≠ 0, m ≠ 0 — General Computation
- **Role**: Complex operations, transformations
- Could represent function application, composition, etc.
- Need to determine semantics

### The Challenge: Enumeration

We need a numbering scheme that:
1. **Covers all matrices** (bijection with integers)
2. **Preserves semantic regions** (operations on same region stay related)
3. **Is computationally tractable** (can convert ID ↔ structure efficiently)

### Possible Enumeration Strategies

#### Strategy A: Region-Priority Ordering

Enumerate by semantic importance:
```
Priority 1: Empty (0)
Priority 2: Pure positives {(0,1), (0,2), ...}
Priority 3: Pure negatives {(1,0), (2,0), ...}
Priority 4: Pure diagonals {(1,1), (2,2), ...}
Priority 5: Mixed sets...
```

**Problem**: Complex to compute, not obviously bijective with N.

#### Strategy B: Signed Integer Encoding

Use signed integers where:
- Positive integers → graphs with only (0, n) edges
- Negative integers → graphs with only (n, 0) edges
- Zero → empty graph
- Other integers → mixed graphs

```
 0 → {}
 1 → {(0, 1)}
 2 → {(0, 2)}
-1 → {(1, 0)}
-2 → {(2, 0)}
 3 → {(0, 1), (0, 2)}  or  {(1, 1)}?
```

**Challenge**: How to handle mixed sets and diagonals?

#### Strategy C: Factored Representation

Represent graph ID as product of primes or tuple:
```
ID = (positive_component, negative_component, diagonal_component, other_component)
```

Each component could use its own encoding.

**Challenge**: Not a single integer anymore.

#### Strategy D: Interleaved Enumeration

Interleave different regions in the integer sequence:
```
0 → empty
1 → {(0, 1)}       (first positive)
2 → {(1, 0)}       (first negative)
3 → {(1, 1)}       (first diagonal)
4 → {(0, 2)}       (second positive)
5 → {(2, 0)}       (second negative)
6 → {(2, 2)}       (second diagonal)
7 → {(0, 1), (1, 0)}  (first mixed)
...
```

**Pro**: Single integer, covers all cases
**Con**: Complex enumeration formula

---

## Semantic Interpretation Deep Dive

### Positive (0, n) as Iteration

Consider `(0, n)` as "repeat n times":
```
eval((0, 1), x) = succ(x)     -- add one layer
eval((0, 2), x) = succ(succ(x))
eval((0, n), x) = n-fold application of successor
```

A graph with multiple positive edges:
```
{(0, 2), (0, 3)} = "produce 2 and produce 3" = produce 5? or parallel production?
```

### Negative (n, 0) as Pattern Matching

Consider `(n, 0)` as "match and consume n":
```
eval((1, 0), succ(x)) = x     -- remove one layer
eval((2, 0), succ(succ(x))) = x
eval((n, 0), m-deep structure) = (m-n)-deep structure if m ≥ n, else fail
```

This gives us subtraction / pattern matching:
```
{(0, 5), (3, 0)} applied to x = add 5, remove 3 = net +2
```

### Diagonal (n, n) as Data Tags

The diagonal could mark data variants:
```
(1, 1) = "this is variant 1"
(2, 2) = "this is variant 2"

List example:
  Cons = (1, 1)
  Nil  = (2, 2)

  [a, b] = {(1,1), (0, a), (next, [b])}
         = {(1,1), (0, a), (?, {(1,1), (0,b), (?, {(2,2)})})}
```

### Off-Diagonal (n, m) as Transformation

For n ≠ m, n ≠ 0, m ≠ 0:
```
(n, m) could mean:
  - "transform structure-n into structure-m"
  - "if you have n, produce m"
  - function/morphism from n to m
```

---

## Open Questions

1. **What is (0, 0)?**
   - The origin is special. Is it identity? Self-reference? Undefined?
   - In the space-filling curve approach, `{(0,0)}` is a valid graph.
   - In the semantic approach, it might need special handling.

2. **How do multiple edges interact?**
   - `{(0, 2), (0, 3)}` — additive? parallel? sequential?
   - `{(1, 0), (2, 0)}` — consume 1 then 2? consume either?
   - `{(0, n), (m, 0)}` — produce then consume? net effect?

3. **How to handle the "other" region systematically?**
   - (n, m) for n ≠ m needs clear semantics
   - Could be: conditionals, recursion, higher-order ops

4. **Can we maintain bijectivity while preserving semantics?**
   - The space-filling curve is bijective but semantics-free
   - Adding semantics might break clean enumeration

5. **What about nested structure?**
   - Edge (a, b) where a, b are themselves complex graphs
   - How does semantic region of (a, b) relate to semantics of a and b?

---

## Comparison Summary

| Aspect | Space-Filling Curve | Semantic Regions |
|--------|---------------------|------------------|
| Bijective | Yes | Needs careful design |
| Semantic meaning | None inherent | Built-in |
| Complexity | Moderate | Higher |
| Natural numbers | Convention-based | Region-based |
| Negatives/destruction | Not native | Native |
| Data constructors | Convention-based | Diagonal region |

---

## Next Steps

1. **Formalize the semantic interpretation** of each region
2. **Design an enumeration scheme** that covers all matrices while respecting regions
3. **Define interaction rules** for graphs with edges in multiple regions
4. **Implement prototype** in Python to test the scheme
5. **Prove properties** in Lean (bijectivity, computational behavior)

---

---

## Approach 3: Polarized Type Syntax (Haskell-like with Negatives)

### Motivation

In Haskell, we define data types with constructors:

```haskell
data Nat = Zero | Succ Nat
data List a = Nil | Cons a (List a)
```

But these are all **positive** — they build structure. What if we had **negative constructors** that destruct/consume structure?

### Polarized Constructor Syntax

```
-- Positive constructors (build)
data Nat where
  Zero : Nat                    -- (0, 0) diagonal: base case
  Succ : Nat -> Nat             -- (0, n) row: add structure

-- Negative constructors (consume/pattern match)
codata Nat where
  pred : Nat -> Nat             -- (n, 0) column: remove structure
  isZero : Nat -> Bool          -- pattern match, return info
```

### Duality Table

| Positive (0, n)      | Negative (n, 0)        | Meaning |
|----------------------|------------------------|---------|
| `Succ`               | `pred`                 | +1 / -1 |
| `Cons head tail`     | `uncons` → head, tail  | build / destruct list |
| `Just x`             | `fromJust`             | wrap / unwrap Maybe |
| `Left x` / `Right y` | `either f g`           | inject / eliminate Either |

### The (n, n) Diagonal as Type Tags

The diagonal distinguishes different types/constructors:

```
(1, 1) = Nat tag
(2, 2) = Bool tag
(3, 3) = List tag
(4, 4) = Maybe tag
...
```

A value carries its type tag:

```
-- The number 2 as a Nat:
{(1,1), (0, {(1,1), (0, {(1,1)})})}
   ^         ^         ^
   Nat tag   Nat tag   Nat tag (Zero = just the tag)
```

### Full Example: Encoding `Cons 'A' Nil`

```
List Char structure:
  Cons = positive constructor at (0, n)
  Nil  = base case at diagonal

Nil  = {(3, 3)}                           -- List tag, no content
Cons = {(3, 3), (0, head), (0, tail)}     -- List tag + two fields

Char 'A' = {(4, 4), (0, 65)}              -- Char tag + codepoint

Cons 'A' Nil:
{
  (3, 3),                    -- I'm a List
  (0, {(4,4), (0, 65)}),     -- head = Char 'A'
  (0, {(3, 3)})              -- tail = Nil
}
```

But wait — how do we distinguish the two `(0, ...)` edges? We need field indices.

### Refined Encoding with Field Positions

Use the positive row for field indexing:

```
(0, 1) = first field (e.g., head)
(0, 2) = second field (e.g., tail)
(0, n) = nth field

Structure becomes:
  type_tag at (t, t)
  field_1  at (0, 1) pointing to value_1
  field_2  at (0, 2) pointing to value_2
  ...
```

But this conflates field index with value. Alternative:

### Two-Level Encoding

**Level 1: Structure skeleton**
```
(0, n)  = "slot n exists"
(n, 0)  = "expect to receive at slot n"
(n, n)  = "type tag n"
```

**Level 2: Values in slots**
Each slot points to another graph (the value).

```
Cons 'A' Nil =
{
  (3, 3),           -- List type tag
  (0, 1),           -- slot 1 exists (head)
  (0, 2),           -- slot 2 exists (tail)
  (1, char_A_id),   -- slot 1 contains Char 'A'
  (2, nil_id)       -- slot 2 contains Nil
}
```

Here `(0, n)` declares a slot, and `(n, value)` fills it.

### Negative Constructors in Action

A pattern match / destructor:

```haskell
case list of
  Nil -> defaultVal
  Cons h t -> f h t
```

Encoded as:

```
{
  (3, 0),           -- consume a List
  (1, 0),           -- extract slot 1 (head)
  (2, 0),           -- extract slot 2 (tail)
  ...               -- what to do with extracted values?
}
```

The `(n, 0)` edges say "I expect something in slot n, give it to me."

### Interaction Semantics

When a positive graph meets a negative graph:

```
Positive: {(3,3), (0,1), (0,2), (1, A), (2, B)}  -- Cons A B
Negative: {(3,0), (1,0), (2,0)}                  -- destruct List

Interaction:
  (3,3) ↔ (3,0) : type tags match ✓
  (0,1) ↔ (1,0) : slot 1 declared ↔ slot 1 demanded → extract A
  (0,2) ↔ (2,0) : slot 2 declared ↔ slot 2 demanded → extract B

Result: bindings {slot1 → A, slot2 → B}
```

This is like **cut elimination** in sequent calculus or **beta reduction** in lambda calculus.

### The Off-Diagonal (n, m) Region

Now we can assign meaning to general `(n, m)`:

```
(n, m) where n ≠ m, n > 0, m > 0:
  "Transform what's in slot n and put result in slot m"

Or:
  "Slot n connects to slot m" (function application, piping)
```

Example — function that swaps first two elements:

```
swap : (a, b) -> (b, a)

{
  (1, 0),   -- demand slot 1 (get first element)
  (2, 0),   -- demand slot 2 (get second element)
  (0, 1),   -- provide slot 1
  (0, 2),   -- provide slot 2
  (1, 2),   -- old slot 1 goes to new slot 2
  (2, 1),   -- old slot 2 goes to new slot 1
}
```

### Summary of Polarized Regions

```
        m (output/positive)
        0   1   2   3   ...
      ┌───┬───┬───┬───┬───
    0 │ ∅ │ +1│ +2│ +3│      (0,m): provide slot m
  n   ├───┼───┼───┼───┼───
(in/  │-1 │ T₁│1→2│1→3│      (n,0): demand slot n
neg)1 │   │   │   │   │      (n,n): type tag n
      ├───┼───┼───┼───┼───   (n,m): connect slot n → slot m
    2 │-2 │2→1│ T₂│2→3│
      ├───┼───┼───┼───┼───
    3 │-3 │3→1│3→2│ T₃│
      └───┴───┴───┴───┴───
```

### Correspondence to Logic

This maps to **linear logic** / **classical logic**:

| Graph Region | Logic | Meaning |
|--------------|-------|---------|
| (0, n) | Positive proposition | Provide/prove |
| (n, 0) | Negative proposition | Demand/use |
| (n, n) | Axiom / Identity | Type itself |
| (n, m) | Cut / Application | Connect proof to use |

---

## Appendix: Notation Reference

```
{}              Empty graph, ID = 0
{(a, b)}        Graph with single edge from a to b
{(a,b), (c,d)}  Graph with two edges

(0, n)          Positive/constructor edge
(n, 0)          Negative/destructor edge
(n, n)          Diagonal/data edge
(n, m)          General edge (n≠m, n≠0, m≠0)
```
