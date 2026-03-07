from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from test_eval import FNode, FExpr


class RewriteRulesBase(ABC):
    """Base class for rewrite rule implementations."""
    
    @abstractmethod
    def rewrite_from_input(self, node: "FNode", other: "FNode") -> List["FExpr"]:
        """
        Apply rewrite rules when a node receives input from another node.
        
        Args:
            node: The node that is receiving input
            other: The node providing input
            
        Returns:
            List of expressions after applying rewrite rules
        """
        pass
    
    @abstractmethod
    def match_input(self, node: "FNode", target: "FNode") -> bool:
        """
        Check if a node can match/accept input from a target node.
        
        Args:
            node: The node checking for input compatibility
            target: The target node to match against
            
        Returns:
            True if the input can be matched, False otherwise
        """
        pass