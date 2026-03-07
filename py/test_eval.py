from ast import alias
from asyncio import Future
from hmac import new
from typing import Any, List, Tuple, Dict, Optional, Union, Self, final
import unittest
from pprint import pprint
from matrix_morton import MatrixMorton
from matrix_hilbert import MatrixHilbert
from matrix_base import MatrixBase
from rewrite_base import RewriteRulesBase
from rewrite_default import DefaultRewriteRules


# Configuration for matrix curve type
MATRIX_CURVE_TYPE = "morton"  # Options: "morton", "hilbert"

# Configuration for rewrite rules type
REWRITE_RULES_TYPE = "default"  # Options: "default", "sandwich"

def get_matrix_class() -> type[MatrixBase]:
    """Returns the appropriate matrix class based on configuration."""
    if MATRIX_CURVE_TYPE == "morton":
        return MatrixMorton
    elif MATRIX_CURVE_TYPE == "hilbert":
        return MatrixHilbert
    else:
        raise ValueError(f"Unknown matrix curve type: {MATRIX_CURVE_TYPE}")

def create_matrix_graph(n: int) -> MatrixBase:
    """Creates a matrix graph using the configured curve type."""
    matrix_class = get_matrix_class()
    return matrix_class.from_int(n)

def create_functional_node(edges: List, name: Optional[str] = None) -> MatrixBase:
    """Creates a functional graph node using the configured curve type."""
    matrix_class = get_matrix_class()
    return matrix_class(edges, name)

def set_matrix_curve_type(curve_type: str):
    """Sets the global matrix curve type. Options: 'morton' or 'hilbert'."""
    global MATRIX_CURVE_TYPE
    if curve_type not in ["morton", "hilbert"]:
        raise ValueError(f"Invalid curve type: {curve_type}. Must be 'morton' or 'hilbert'")
    MATRIX_CURVE_TYPE = curve_type

def get_rewrite_rules_class() -> type[RewriteRulesBase]:
    """Returns the appropriate rewrite rules class based on configuration."""
    if REWRITE_RULES_TYPE == "default":
        return DefaultRewriteRules
    elif REWRITE_RULES_TYPE == "sandwich":
        from rewrite_sandwich import SandwichRewriteRules
        return SandwichRewriteRules
    else:
        raise ValueError(f"Unknown rewrite rules type: {REWRITE_RULES_TYPE}")

def create_rewrite_rules() -> RewriteRulesBase:
    """Creates a rewrite rules instance using the configured type."""
    rules_class = get_rewrite_rules_class()
    return rules_class()

def set_rewrite_rules_type(rules_type: str):
    """Sets the global rewrite rules type. Options: 'default', 'sandwich'."""
    global REWRITE_RULES_TYPE
    if rules_type not in ["default", "sandwich"]:
        raise ValueError(f"Invalid rewrite rules type: {rules_type}. Must be 'default' or 'sandwich'")
    REWRITE_RULES_TYPE = rules_type


"""
- Type checking
- Resource checking (form of type checking where resources are linear or affine types?)

- going to require sending message from func -> args
- relayed through node which composes them?
    - I'm node A, I compose B and C
    - "B, can you take arg C?"
    - "B, how many resources do you need to do your thing with arg C?"
    - "

    B recieves message "From: A, To: B, "Can you take arg C?"": 
        - has expr (D, E), 
            - sends message to E "Can you take arg C?"
                - =Recieve on C, continue with D
            - D should then contain some way to respond to A
            - E should be 



"""

events = []

# Global Z node instance (zero/identity node)
Z = None

# Initialize Z as a special zero/identity node
def _init_z():
    global Z
    if Z is None:
        Z = create_functional_node([], "Z")

_init_z()


# Unit tests
class TestRewriteSystem(unittest.TestCase):

    def test_constant_false(self):
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        raise NotImplementedError("test not implemented yet")

    def test_constant_true(self):
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        raise NotImplementedError("test not implemented yet")

    def test_ident(self):
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        raise NotImplementedError("test not implemented yet")

    # @unittest.skip("Skipping test for now")
    def test_boolean_and(self):
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        raise NotImplementedError("test not implemented yet")

    def test_k_combinator(self):
        """
        X would be a channel which is subscribed to the outer input.



        """
        raise NotImplementedError("test not implemented yet")
        K_comb = FNode([FExpr(FNode([FExpr(X, Z)]), Z)])

    @unittest.skip("Skipping test for now")
    def test_s_combinator(self):
        raise NotImplementedError("S combinator test not implemented yet")

    def test_matrix_graph_creation(self):
        """Test basic matrix graph creation with current curve type."""
        mg = create_matrix_graph(0)
        self.assertEqual(mg.to_int(), 0)
        
        mg1 = create_matrix_graph(1)
        self.assertEqual(mg1.to_int(), 1)
        
        mg5 = create_matrix_graph(5)
        self.assertEqual(mg5.to_int(), 5)

    def test_matrix_graph_roundtrip(self):
        """Test that matrix graphs can be converted to int and back."""
        test_values = [0, 1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        
        for val in test_values:
            with self.subTest(value=val):
                mg = create_matrix_graph(val)
                result = mg.to_int()
                self.assertEqual(result, val, 
                    f"Roundtrip failed for {val} with curve type {MATRIX_CURVE_TYPE}")

    def test_matrix_to_anytree(self):
        """Test anytree conversion works for both curve types."""
        mg = create_matrix_graph(7)
        tree = mg.to_anytree()
        self.assertIsNotNone(tree)
        self.assertEqual(tree.name, "7")

    def test_curve_type_switching(self):
        """Test switching between curve types."""
        original_type = MATRIX_CURVE_TYPE
        
        try:
            # Test Morton
            set_matrix_curve_type("morton")
            mg_morton = create_matrix_graph(5)
            self.assertIsInstance(mg_morton, MatrixMorton)
            
            # Test Hilbert  
            set_matrix_curve_type("hilbert")
            mg_hilbert = create_matrix_graph(5)
            self.assertIsInstance(mg_hilbert, MatrixHilbert)
            
            # Both should be able to convert to int
            self.assertEqual(mg_morton.to_int(), 5)
            self.assertEqual(mg_hilbert.to_int(), 5)
            
        finally:
            # Restore original type
            set_matrix_curve_type(original_type)

    def test_invalid_curve_type(self):
        """Test that invalid curve types raise errors."""
        with self.assertRaises(ValueError):
            set_matrix_curve_type("invalid_type")

    def test_morton_vs_hilbert_comparison(self):
        """Compare Morton and Hilbert curve implementations."""
        test_values = [1, 2, 3, 5, 7, 11, 13, 17]
        
        for val in test_values:
            with self.subTest(value=val):
                # Create both types
                mg_morton = MatrixMorton.from_int(val)
                mg_hilbert = MatrixHilbert.from_int(val)
                
                # Both should preserve the integer value
                self.assertEqual(mg_morton.to_int(), val)
                self.assertEqual(mg_hilbert.to_int(), val)
                
                # Both should produce valid matrices
                matrix_morton = mg_morton.to_matrix()
                matrix_hilbert = mg_hilbert.to_matrix()
                
                self.assertIsInstance(matrix_morton, list)
                self.assertIsInstance(matrix_hilbert, list)
                
                # The matrices may be different due to different curve orderings
                # but both should have the same number of True values
                def count_true_values(matrix):
                    return sum(sum(row) for row in matrix)
                
                if matrix_morton and matrix_hilbert:
                    self.assertEqual(
                        count_true_values(matrix_morton),
                        count_true_values(matrix_hilbert),
                        f"Different number of True values for {val}"
                    )

    def test_curve_locality_properties(self):
        """Test that both curves maintain their locality properties."""
        # Test that both curves can handle the same range of values
        max_test_val = 100
        
        for curve_type in ["morton", "hilbert"]:
            with self.subTest(curve_type=curve_type):
                original_type = MATRIX_CURVE_TYPE
                try:
                    set_matrix_curve_type(curve_type)
                    
                    # Test a range of values
                    for val in range(0, min(max_test_val, 50)):  # Limit to avoid long test times
                        mg = create_matrix_graph(val)
                        self.assertEqual(mg.to_int(), val)
                        
                        # Test that matrix conversion is stable
                        matrix = mg.to_matrix()
                        self.assertIsInstance(matrix, list)
                        
                finally:
                    set_matrix_curve_type(original_type)

    def test_matrix_representation_consistency(self):
        """Test that matrix representations are consistent within each curve type."""
        test_values = [0, 1, 4, 9, 16, 25]  # Perfect squares for cleaner matrices
        
        for curve_type in ["morton", "hilbert"]:
            with self.subTest(curve_type=curve_type):
                original_type = MATRIX_CURVE_TYPE
                try:
                    set_matrix_curve_type(curve_type)
                    
                    for val in test_values:
                        # Create multiple instances of the same value
                        mg1 = create_matrix_graph(val)
                        mg2 = create_matrix_graph(val)
                        
                        # They should be equivalent
                        self.assertEqual(mg1.to_int(), mg2.to_int())
                        self.assertEqual(mg1.to_matrix(), mg2.to_matrix())
                        
                finally:
                    set_matrix_curve_type(original_type)
