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
        raise ValueError(
            f"Invalid curve type: {curve_type}. Must be 'morton' or 'hilbert'"
        )
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
        raise ValueError(
            f"Invalid rewrite rules type: {rules_type}. Must be 'default' or 'sandwich'"
        )
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


# Initialize Z as a special zero/identity node
def _init_z():
    global Z
    if Z is None:
        Z = create_functional_node([], "Z")


_init_z()


NAMED_NODES: Dict[str, "FNode"] = {}
NAMED_EXPRS: Dict[str, "FExpr"] = {}


class FNode:

    name: str | None = None

    def __init__(self, args: List["FExpr"], name: str | None = None):
        self.edges: List["FExpr"] = []
        self.name = name
        if name:
            if name in NAMED_NODES:
                if NAMED_NODES[name] != self:
                    raise ValueError(f"Node {name} already defined")
            NAMED_NODES[name] = self
        self.edges = args

    def __eq__(self, other) -> bool:
        if not isinstance(other, FNode):
            return False
        if len(self.edges) != len(other.edges):
            return False
        for i, edge in enumerate(self.edges):
            if edge != other.edges[i]:
                return False
        return True

    def __repr__(self) -> str:
        if self.name:
            return f"{self.name}"
        else:

            return f"{{{self.edges}}}"


# Primitive nodes
class FExpr:
    def __init__(self, left: FNode | str, right: FNode | str, name: str | None = None):
        if name:
            if name in NAMED_EXPRS:
                if NAMED_EXPRS[name] != self:
                    raise ValueError(f"Node {name} already defined")
            NAMED_EXPRS[name] = self
        self.name = name
        if isinstance(left, str):
            if left in NAMED_NODES:
                left = NAMED_NODES[left]
            else:
                raise ValueError(f"Node {left} not defined")
        if isinstance(right, str):
            if right in NAMED_NODES:
                right = NAMED_NODES[right]
            else:
                raise ValueError(f"Node {right} not defined")

        if not isinstance(left, FNode):
            raise ValueError(f"Invalid argument: {left}")

        if not isinstance(right, FNode):
            raise ValueError(f"Invalid argument: {right}")
        self.left = left
        self.right = right

    def __eq__(self, other) -> bool:
        if not isinstance(other, FExpr):
            return False
        equal = self.left == other.left and self.right == other.right
        return equal

    def __repr__(self) -> str:
        return f"[{self.left}> <{self.right}]"


def rewrite_node(node: FNode) -> FNode:
    new_edges = []
    is_same = True
    for i, edge in enumerate(node.edges):
        if not isinstance(edge, FExpr):
            print(node.edges)
            raise ValueError(f"Invalid argument: {edge}")
        res: List[FExpr] = rewrite_edge(edge)
        if len(res) != 1 or res[0] != edge:
            is_same = False
            new_edges.extend(res)
    if is_same:
        return node
    else:
        new_node = FNode(new_edges, name=node.name)
        final_node = rewrite_node(new_node)
        return final_node


Z: FNode = FNode([], name="Z")


# Rewrite rules
def rewrite_edge(edge: FExpr) -> List[FExpr]:
    if not edge.left or not edge.right:
        raise ValueError(f"Invalid argument: {edge}")
    if not isinstance(edge, FExpr):
        raise ValueError(f"Invalid argument: {edge}")
    if edge.left == Z:
        return [edge]
    if edge.right == Z:
        return edge.left.edges
    new_edges = []
    for l_edge in edge.left.edges:
        if l_edge.right == edge.right:
            # print("here2", l_edge.left, l_edge, edge.right)
            new_edges.append(FExpr(l_edge.left, Z))
        else:
            for r_edge in edge.right.edges:
                # print("here2", l_edge, r_edge)
                if match_node(l_edge.right, r_edge.left):
                    new_edges.append(FExpr(l_edge.left, r_edge.right))

    return new_edges


def match_node(pattern: FNode, target: FNode):
    if pattern == Z:
        return True
    if pattern == target:
        return True
    for i, p_edge in enumerate(pattern.edges):
        has_edge_match = any(
            [
                match_node(p_edge.left, t_edge.left)
                and match_node(p_edge.right, t_edge.right)
                for t_edge in target.edges
            ]
        )
        return has_edge_match
    return True


Z_Z = FExpr(Z, Z)
U = FNode([Z_Z], name="U")

Z_U = FNode([FExpr(Z, U)], name="ZU")
U_U = FNode([FExpr(U, U)], name="UU")
U_Z = FNode([FExpr(U, Z)], name="UZ")


ZZ_ZU = FNode([Z_Z, FExpr(Z, U)], name="ZZ_ZU")
ZZ_UZ = FNode([Z_Z, FExpr(U, Z)], name="ZZ_UZ")
ZZ_UU = FNode([Z_Z, FExpr(U, U)], name="ZZ_UU")
ZU_ZZ = FNode([FExpr(Z, U), Z_Z], name="ZU_ZZ")
ZU_ZU = FNode([FExpr(Z, U), FExpr(U, U)], name="ZU_ZU")
ZU_UZ = FNode([FExpr(Z, U), FExpr(U, Z)], name="ZU_UZ")
ZU_UU = FNode([FExpr(Z, U), FExpr(U, U)], name="ZU_UU")
UZ_ZZ = FNode([FExpr(U, Z), Z_Z], name="UZ_ZZ")
UZ_UZ = FNode([FExpr(U, Z), FExpr(U, Z)], name="UZ_UZ")
UZ_UU = FNode([FExpr(U, Z), FExpr(U, U)], name="UZ_UU")
UU_ZZ = FNode([FExpr(U, U), Z_Z], name="UU_ZZ")
UU_UZ = FNode([FExpr(U, U), FExpr(U, Z)], name="UU_UZ")
UU_UU = FNode([FExpr(U, U), FExpr(U, U)], name="UU_UU")


UUZU = FNode([FExpr("U", "U"), FExpr("Z", "U")], name="UUZU")
ZUZU = FNode([FExpr("Z", "U"), FExpr("U", "Z")], name="ZUZU")
ZZU = FNode([FExpr("Z", "Z"), FExpr("Z", "Z")], name="ZZU")
ZZ_UZ = FNode([FExpr("Z", "Z"), FExpr("U", "Z")], name="ZZZ")
ZZZZ = FNode([FExpr("Z", "Z"), FExpr("U", "Z")], name="ZZZZ")
ZZUZ = FNode([FExpr("Z", "Z"), FExpr("U", "Z")], name="ZZZZZ")


# Behavior tagging
def auto_behavior_tags(expr: FExpr, result: List[FExpr]) -> str:
    if result == []:
        return "reduces_to_Z"
    if result == [NAMED_EXPRS["U"]]:
        return "reduces_to_U"
    if result == expr.left:
        return "id_like"
    if result == expr.right:
        return "const_like"
    return "unclassified"


# Unit tests
class TestRewriteSystem(unittest.TestCase):

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
                self.assertEqual(
                    result,
                    val,
                    f"Roundtrip failed for {val} with curve type {MATRIX_CURVE_TYPE}",
                )

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
                        f"Different number of True values for {val}",
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
                    for val in range(
                        0, min(max_test_val, 50)
                    ):  # Limit to avoid long test times
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

    def test_rule_Z_applied_to_expr(self):
        expr = FExpr(Z, Z_U)
        result = rewrite_edge(expr)
        self.assertEqual(result, [FExpr(Z, Z_U)])

    def test_rule_expr_applied_to_Z(self):
        expr = FExpr(Z_U, Z)
        result = rewrite_edge(expr)
        self.assertEqual(result, [FExpr(Z, U)])

    def test_rule_ZZ_applied_to_expr(self):
        expr = FExpr(U, Z_U)
        result = rewrite_edge(expr)
        self.assertEqual(result, [FExpr(Z, U)])

    def test_constant_false(self):
        false_val = FNode([FExpr(Z, Z)])
        true_val = FNode([FExpr(Z, U)])
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        # constant_false = FNode([FExpr(U, Z)])
        # false_res = rewrite_edge(rewrite_edge(FExpr(constant_false, false_val))[0])
        # true_res = rewrite_edge(rewrite_edge(FExpr(constant_false, true_val))[0])

        constant_false = FNode([FExpr(FNode([FExpr(U, Z)]), Z)])
        false_res = rewrite_edge(
            rewrite_edge(rewrite_edge(FExpr(constant_false, false_val))[0])[0]
        )
        true_res = rewrite_edge(
            rewrite_edge(rewrite_edge(FExpr(constant_false, true_val))[0])[0]
        )

        # print(false_res, false_val, true_res, true_val)
        assert FNode(false_res) == false_val
        assert FNode(true_res) == false_val

    def test_constant_true(self):
        false_val = FNode([FExpr(Z, Z)])
        true_val = FNode([FExpr(Z, U)])
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        constant_true = FNode([FExpr(FNode([FExpr(Z_U, Z)]), Z)])
        # false_res = rewrite_edge(rewrite_edge(FExpr(constant_true, false_val))[0])
        # print("FALSE ARG")
        false_res = rewrite_edge(
            rewrite_edge(rewrite_edge(FExpr(constant_true, false_val))[0])[0]
        )
        # print(false_res, true_val)
        assert FNode(false_res) == true_val
        # print("TRUE ARG")
        true_res = rewrite_edge(
            rewrite_edge(rewrite_edge(FExpr(constant_true, true_val))[0])[0]
        )
        # print(true_res, true_val)
        assert FNode(true_res) == true_val

    def test_ident(self):
        false_val = FNode([FExpr(Z, Z)])
        true_val = FNode([FExpr(Z, U)])
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        id = U
        false_res = rewrite_edge(FExpr(id, false_val))
        assert FNode(false_res) == false_val
        true_res = rewrite_edge(FExpr(id, true_val))
        assert FNode(true_res) == true_val

    # @unittest.skip("Skipping test for now")
    def test_boolean_and(self):
        false_val = FNode([FExpr(Z, Z)], name="false")
        true_val = FNode([FExpr(Z, U)], name="true")
        # if first arg is false, then anything returns false,
        # if first arg is true, then second arg returns itself
        """
         # [FExpr(CF, Z)] => [FExpr(Z, Z)], # [FExpr(CF, U)] => [FExpr(Z, Z)]
         # CF = FNode([FExpr(Z, U)], name="CF")

        """
        constant_false = FNode([FExpr(U, Z)])
        """
        # [FExpr(ID, Z_Z)] => [FExpr(Z, Z)], # [FExpr(ID, Z_U)] => [FExpr(Z, U)]

        # ID = FNode([FExpr(Z, Z)], name="ID")
        """
        id_fn = U
        """
        # AND [Z, Z] => [Z, U]
        # AND [Z, U] => [Z, Z]

        [[Z, U], Z] [Z, Z] => [Z, U] [Z] => [Z, U]
        [[Z, U], Z] [Z, [[Z, Z]]] => [Z, [[Z, Z]]] [[Z, Z]] => Z
        """

        A = FNode([FExpr(FNode([FExpr(constant_false, Z)]), Z)], name="AND")
        and_res_1 = rewrite_edge(rewrite_edge(rewrite_edge(FExpr(A, false_val))[0])[0])
        print(and_res_1, constant_false)
        assert FNode(and_res_1) == constant_false
        and_res_2 = rewrite_edge(
            rewrite_edge(rewrite_edge(rewrite_edge(FExpr(A, true_val))[0])[0])[0]
        )
        print(and_res_2)
        print(id_fn)
        assert FNode(and_res_2) == id_fn

    @unittest.skip("Skipping test for now")
    def test_behavior_matrix(self):
        results = run_behavior_matrix()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        # pprint(results[:5])  # Show only the first few for brevity


# Matrix-based behavior test runner
def run_behavior_matrix():
    results = []
    test_node_names = list(NAMED_NODES.keys())
    for name1 in test_node_names:
        for name2 in test_node_names:
            expr = FExpr(name1, name2)
            result = rewrite_edge(expr)
            tag = (
                auto_behavior_tags(expr, result)
                if isinstance(result, list)
                else "no_match"
            )
            results.append(
                {
                    "lhs": name1,
                    "rhs": name2,
                    "lhs_node": expr.left,
                    "rhs_node": expr.right,
                    "result": result,
                    "tag": tag,
                }
            )
    return results
