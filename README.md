# graphlang

This is a collection of open-ended experiments related to exploring programming langauge concepts such as term rewriting, [Unison](https://www.unison-lang.org/)-style hash-consing the AST, numerical encodings based on the dependency-graph structure of programs etc. 

Some explorations include: 
- in python, using a space-filling curves like Morton ordering and Hilbert to enumerate possible dependecy graphs and assign numbers to each graph for a numeric encoding [Enumerating graphs](./artifacts/FastCounting_corrected.mp4)
- in c++ hash-consing a graph from a yaml document.. an initial attempt before realizing I need more flexibility while hammering things out
- in lean, trying to develop a co-inductive model of the bitstring representation of the dependency graph, allowing potential representations of infinite bitstrings
- in rust, trying to develop a distributed/p2p wasm-based version of the concept with the goal of distributing dependencies via DHT 

Avenues I'm trying to explore: 
- homomorphic encodings of fixpoints to avoid including addresses outside the hierarchically finite hash-consing of the computation tree for cyclic graphs
- using 2-adics/infinite bitstrings and operations as a model for a coinductive language
- using operations such as geometric product for evaluation mechanism to provide clear geometric interpretation of computation

