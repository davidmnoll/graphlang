Explanation: 

A programming language can be represented by its syntax tree.  

A syntax tree consists of some finite number of expressions, consisting of one of some finite number of term types on the left combined with some term on the right, some of which may also be expressions, or else one of some finite number of primitive objects of an appropriate type.  If more than one argument is required for the expression to be well-formed, the terms on the right can be rewritten as a tuple and considered as a single object.  

Since any turing complete language in theory can express any program in any other turing complete language, we can say that any computation can be represented as such a "graph"-like strcuture. 

N1:
- [N1.1L, N1.1R]
- [N1.2L, N1.2R]
- [N1.3L, N1.3R]

A node of the graph could be represented with the preceding form.  N1.1L could mean something like "function application", and N1.1R might be a tuple containing a reference to the function being applied as well as its arguments.  


However there's another way to look at this as well.  If you look at the primitive element of any programming language, they ultimately form functions of some kind.  In a lisp language, one of the function is "apply".  There are also cdr and car which are functions which may be implemented in assembly.  For those not familiar with functional lanugages, constructing data looks can look similar to function application as data is built up from "data constructors" which are basically functions that don't get reduced.  There is no substitution of arguments into a body, the arguments just are appended as nodes to the syntactic element and possibly later converted to a primitive of some kind.  

This treatment of the lowest level elements as functions and dependency graphs is deeper than just a superficial element of functional languages though.  Assembly similarly can be represented this way, and ultimately it constructs not just a dependency graph of computations, but also physcial mechanisms which instantiate those computations.  This gives some insight into the nature of computations and information which that they are physical transformations.

All of this is to say, rather than put the primitive type "function application" on the left and put the function reference on the right along with the arguments.  We *should* be able to construct a language in which the function is referenced on the left.  So in the tree the left would no longer be a finite set of terms, but would be infinite just like the right. 

This means the N1.1L and N1.1R would both be graphs in their own rights.  But in this case, where are the primitive elements they're built up from?  We already have them (sort of): 
- the empty node
- the operation of parallel compostion
- the ability to construct terms with a left and a right
- some set of rewrite rules*
* It is probably provable that these rewrite rules should exist, but I'm not sure how to prove it and I haven't found them yet
  
Now we have a mathematical object from first principles that should theoretically be able to represent any computation.  Each element in the graph can represent some combination of previously constructed nodes.  We now can build up expressions as a left + right node, and create more nodes as sets of these expressions. 

0 - Empty: {}

0_0 (a.k.a. "1") - Unit: { ({}, {}) }
0_1 - { ({}, { ({}, {}) })  }
1_0 - { ({ ({}, {}) }, {}) }
1_1

0_1-0_0 - { ({}, { ({}, {}) }), ({}, {}) }
1_0-0_0 -
1_1-0_0
1_1-0_1
1_1-1_0

0_0-0_1-1_0
0_0-0_1-1_1
0_0-1_0-1_1
0_1-1_0-1_1

0_0-0_1-1_0-1_1


We can keep going though.  If we assign a number to each node, We can represent them as an adjacency matrix.  Each "expression" is represented by a 1 in the cell corresponding to the key-value pair.  The row could be indexed by the integer corresponding to the key and the column could be indexed by the integer corresponding to the value.  So each node is both an integer and a matrix.  Each coordinate is an expression. 

For instance we could represent the node: 0_0-0_1-1_1 as 
   0  1 
0 [1, 1]
1 [0, 1]

This would also be added on to the matrix as a new column to reference. And so new layers would be added in with a new maximum depth

[1, 2, 3, 3]
[2, 2, 3, 3]
[3, 3, 3, 3]
[3, 3, 3, 3]

The size of the matrix is then 2^(2^n) where n represents the maximum depth of elements.  This happens to correspond to the number of boolean functions that can be done for n input bits as well, so that's a hint that perhaps we're not far off the trail in considering that these can effectively represent computations. 

We've now unlocked some capabilities.  We can start to consider how various matrix operations map to this domain.  We can explore developing our rewrite rules as matrix operations.  We can also explore the properties of our matrix, and play with different ways of numbering the columns which may provide more insight.  

First thing to notice is that the diagonal is the same node on the left and right. 

Another thing that one might notice is that there's a "pascal's triangle" flavor to the above listing of expressions for the 2 levels of depth.  There's a 1 - 4 - 6 - 4 - 1 sequence in the number of nodes with a given number of expressions.  That's a pretty straightforward consequence of the fact that we're iterating over all possible values of the matrix, but still deeper patterns may show up depending on which numberings we choose for the nodes. 

One set of evaluation rules I considered was that if the left side were deeper than the right, then it would be considered "void" or not return a value.  I was considering this to behave like pattern matching.  The node on the left would "eat" from the node on the right until it was exhausted and return whatever was on the right.  On some level this behavior feels like when the left is larger, it's like a negative number, and it means that any expression on the lower diagonal half of the matrix would be "negative" in this way. 

Another consideration is: what if we consider that a single key can only be reused once?  These sparse matrices might have interesting behavior when recombined in various ways.  2x2 matrices correspond to linear transformations, which can also be represented by a complex number.  Perhas these computations could be viewed as chains of linear transformations and represented as sets of complex numbers, opening up a new model and form of computation.


2x2 matrices correspond to linear transformations, which can also be represented by a complex number.  Perhas these computations could be viewed as chains of linear transformations and represented as sets of complex numbers, opening up a new model and form of computation.

This is a bit more out there, and maybe I just had too much coffee this morning, but I'm thinking that perhaps these expression can also be modeled as gaussian integers, and the matricies could be mapped to sets of them.  This could lead to some interesting rewriting schemes based on prime factorization etc.  The fact that the matrix gives a representation of an expression as 2 integers makes me think it's defintiely possible, the question is whether it's possible to do in a productive way.  
