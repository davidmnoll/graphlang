from typing import List, TYPE_CHECKING
from rewrite_base import RewriteRulesBase

if TYPE_CHECKING:
    from matrix_base import MatrixBase, MExpr


class DefaultRewriteRules(RewriteRulesBase):
    """Default implementation of rewrite rules extracted from original FNode logic."""
    
    def rewrite_from_input(self, node: "MatrixBase", other: "MatrixBase") -> List["MExpr"]:
        """
        Apply default rewrite rules when a node receives input from another node.
        This is the original logic from FNode.rewrite_from_input method.
        """
        # Import here to avoid circular imports
        from test_eval import Z
        
        if not other:
            raise ValueError(f"Invalid argument: other node is None")
        
        if node == Z:
            # If this node is Z (zero/identity), return the edge with other
            return [(node, other)]
        
        if other == Z:
            # If other is Z, return this node's entries
            return node.entries
        
        new_edges = []
        for l_edge in node.entries:
            if len(l_edge) >= 2 and l_edge[1] == other:
                # If the right side of left edge matches other, create new edge with Z
                new_edges.append((l_edge[0], Z))
            else:
                # Try to match with other's entries
                for r_edge in other.entries:
                    if len(l_edge) >= 1 and len(r_edge) >= 1:
                        if hasattr(l_edge[0], 'match_input') and l_edge[0].match_input(r_edge[0]):
                            new_edges.append((l_edge[0], r_edge[1]))
        
        return new_edges
    
    def match_input(self, node: "MatrixBase", target: "MatrixBase") -> bool:
        """
        Check if a node can match/accept input from a target node.
        This is the original logic from FNode.match_input method.
        """
        # Import here to avoid circular imports  
        from test_eval import Z
        
        if node == Z:
            return True
        
        if node == target:
            return True
        
        # Check if any entry in this node can match any entry in target
        for i, p_edge in enumerate(node.entries):
            has_edge_match = any([
                len(p_edge) >= 2 and len(t_edge) >= 2 and
                hasattr(p_edge[0], 'match_input') and hasattr(p_edge[1], 'match_input') and
                p_edge[0].match_input(t_edge[1]) and
                p_edge[1].match_input(t_edge[1])
                for t_edge in target.entries
            ])
            if has_edge_match:
                return True
        
        return False