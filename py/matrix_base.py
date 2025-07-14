from typing import List, Tuple, Union, Optional, Dict
from abc import ABC, abstractmethod
from anytree import Node, RenderTree

import matrix_viz


type MExpr = Tuple["MatrixBase", "MatrixBase"]


class MatrixBase(ABC):
    """Base class for matrix-based graph representations with functional node capabilities."""

    def __init__(self, edges: List["MExpr"], name: Optional[str] = None):
        """
        Initialize a graph node.
        
        Args:
            edges: List of expressions (edges) for the node
            name: Optional name for the node
        """
        self.name = name
        self.node_map: Dict[str, "MatrixBase"] = {}
        self.alias_map: Dict[str, "MatrixBase"] = {}
        self.entries = edges
            
        if name:
            if name in self.node_map:
                if self.node_map[name] != self:
                    raise ValueError(f"Node {name} already defined")
            self.node_map[name] = self

    @classmethod
    def from_int(cls, n: int):
        """
        Create a matrix-based graph node from an integer.
        
        Args:
            n: Integer value to convert to matrix representation
        """
        instance = cls.__new__(cls)
        instance.name = None
        instance.node_map = {}
        instance.alias_map = {}
        matrix = instance.get_matrix_from_int(n)
        instance.entries = instance.entries_from_matrix(matrix)
        return instance

    @abstractmethod
    def get_matrix_from_int(self, n: int) -> List[List[bool]]:
        """Convert integer to matrix using specific curve ordering."""
        pass

    @abstractmethod
    def matrix_to_int(self, matrix: List[List[bool]]) -> int:
        """Convert matrix to integer using specific curve ordering."""
        pass

    def __repr__(self):
        if self.name:
            return f"{self.name}"
        else:
            class_name = self.__class__.__name__
            repr_str = f"{class_name}({self.to_int()}) {'-' if len(self.entries) else ''} \n"
            for src, dst in self.entries:
                repr_str += f"{src.to_int()} -> {dst.to_int()}, \n"
            return repr_str
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, MatrixBase):
            return False
        if len(self.entries) != len(other.entries):
            return False
        for i, entry in enumerate(self.entries):
            if entry != other.entries[i]:
                return False
        return True

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.entries, key=str)))

    def to_matrix(self) -> List[List[bool]]:
        if not self.entries:
            return []

        max_index = max(max(e[0].to_int(), e[1].to_int()) for e in self.entries)
        dim = 1 << (max_index.bit_length())
        matrix = [[False for _ in range(dim)] for _ in range(dim)]

        for src, dst in self.entries:
            i, j = src.to_int(), dst.to_int()
            matrix[i][j] = True
        return matrix

    def to_int(self) -> int:
        matrix = self.to_matrix()
        return self.matrix_to_int(matrix)

    def to_anytree(self, label: Union[str, None] = None) -> Node:
        """
        Recursively convert matrix graph into an anytree.Node.
        If the graph is a leaf, return a node with its index.
        """
        name = f"{label:}{self.to_int()}" if label else f"{self.to_int()}"
        root = Node(name)

        for i, (src, dst) in enumerate(self.entries):
            edge_label = f"{src.to_int()} → {dst.to_int()}"
            child1 = src.to_anytree(f"L{i}:")
            child2 = dst.to_anytree(f"R{i}:")
            child1.parent = root
            child2.parent = root
        return root

    def print_anytree(self):
        tree_root = self.to_anytree()
        for pre, _, node in RenderTree(tree_root):
            print(f"{pre}{node.name}")

    def entries_from_matrix(self, matrix: List[List[bool]]) -> List[Tuple["MatrixBase", "MatrixBase"]]:
        entries = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j]:
                    entries.append((self.__class__.from_int(i), self.__class__.from_int(j)))
        return entries

    def rewrite(self):
        """Apply rewrite rules to this node."""
        # Import here to avoid circular imports
        from test_eval import create_rewrite_rules
        
        if not hasattr(self, '_rewrite_rules'):
            self._rewrite_rules = create_rewrite_rules()
        
        new_entries = []
        is_same = True
        
        for i, entry in enumerate(self.entries):
            if not isinstance(entry, tuple):
                raise ValueError(f"Invalid entry: {entry}")
            
            res: List[MExpr] = self._rewrite_rules.rewrite_from_input(entry[0], entry[1])
            if len(res) != 1 or res[0] != entry:
                is_same = False
                new_entries.extend(res)
            else:
                new_entries.append(entry)
        
        if is_same:
            return self
        else:
            new_node = self.__class__(new_entries, name=self.name)
            final_node = new_node.rewrite()
            return final_node

    def rewrite_from_input(self, other: "MatrixBase") -> List[MExpr]:
        """Apply rewrite rules when receiving input from another node."""
        if not hasattr(self, '_rewrite_rules'):
            from test_eval import create_rewrite_rules
            self._rewrite_rules = create_rewrite_rules()
        return self._rewrite_rules.rewrite_from_input(self, other)

    def match_input(self, target: "MatrixBase") -> bool:
        """Check if this node can accept input from target node."""
        if not hasattr(self, '_rewrite_rules'):
            from test_eval import create_rewrite_rules
            self._rewrite_rules = create_rewrite_rules()
        return self._rewrite_rules.match_input(self, target)