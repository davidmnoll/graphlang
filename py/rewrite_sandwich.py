from typing import List, TYPE_CHECKING
from rewrite_base import RewriteRulesBase

if TYPE_CHECKING:
    from matrix_base import MatrixBase, MExpr


class SandwichRewriteRules(RewriteRulesBase):
    """
    Rewrite rules where if the left side is not void/null, then for each pair 
    (L.L, L.R), a new node is created from the resulting expressions where 
    the right node is sandwiched between the two.
    """
    
    def rewrite_from_input(self, node: "MatrixBase", other: "MatrixBase") -> List["MExpr"]:
        """
        Create rewrite expressions where the right node is sandwiched between
        left node components.
        """
        # Import here to avoid circular imports
        from test_eval import Z
        
        result = []
        
        # Check if left side (node) is not void/null/empty
        if node and node != Z and hasattr(node, 'entries') and node.entries:
            # For each pair (L.L, L.R) in the left node's structure
            for left_entry in node.entries:
                if len(left_entry) >= 2:
                    left_left = left_entry[0]   # L.L
                    left_right = left_entry[1]  # L.R
                    
                    # Create new node where right (other) is sandwiched between L.L and L.R
                    # Structure: L.L -> other -> L.R
                    if other:
                        # First connection: L.L -> other
                        result.append((left_left, other))
                        
                        # Second connection: other -> L.R  
                        result.append((other, left_right))
                        
                        # Optional: Also create direct L.L -> L.R connection
                        # to maintain original structure
                        result.append((left_left, left_right))
        
        return result
    
    def match_input(self, node: "MatrixBase", target: "MatrixBase") -> bool:
        """
        Check if this rewrite rule applies.
        Returns True if left node is not void and has structure to work with.
        """
        # Import here to avoid circular imports
        from test_eval import Z
        
        # Match if left node exists and has entries (not void/null/Z)
        if node and node != Z and hasattr(node, 'entries') and node.entries:
            return True
        return False