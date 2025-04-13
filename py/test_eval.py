from typing import Any, List, Tuple, Dict, Optional, Union, Self
import unittest
from pprint import pprint



NAMED_NODES: Dict[str, 'FNode'] = {
}

class FNode: 

    name: str | None = None

    def __init__(self, args: List['FExpr'], name: str | None = None):
        self.edges: List['FExpr'] = []
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
        return f"FNode({self.edges}, name={self.name})"



# Primitive nodes
class FExpr:
    def __init__(self, left: FNode | str, right: FNode | str):
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
        return f"FExpr({self.left}, {self.right})"


def rewrite_node(node: FNode) -> FNode:
    new_edges = []
    is_same = True
    for i, edge in enumerate(node.edges):
        res: List[FExpr] = rewrite_edge(edge)
        if len(res) != 1 or res != edge:
            is_same = False
            new_edges.append(res)
    if is_same:
        return node
    else:
        new_node = FNode(new_edges, name=node.name)
        return new_node
        

Z: FNode = FNode([], name = "Z")


NAMED_EXPRS = {
    "U": FExpr(Z, Z),
}


# Rewrite rules
def rewrite_edge(edge: FExpr) -> List[FExpr]:
    if edge.left == Z:
        return [edge]
    if edge.right == Z:
        return edge.left.edges
    new_edges = []
    for l_edge in edge.left.edges:
        for r_edge in edge.right.edges:
            if match_node(l_edge.right, r_edge.left):
                new_edges.append(FExpr(l_edge.left, r_edge.right))
    return new_edges


def match_node(pattern: FNode, target: FNode):
    if pattern == Z: 
        return True
    if pattern == target:
        return True
    for i, p_edge in enumerate(pattern.edges):
        has_edge_match = any([
            match_node(p_edge.left, t_edge.left)
            and match_node(p_edge.right, t_edge.right) 
            for t_edge in target.edges])
        return has_edge_match
    return True


Z_Z = FNode([FExpr(Z, Z)], name="Z_Z")
U = FNode([FExpr(Z, Z)], name="U")

Z_U = FNode([FExpr(Z, Z_Z)], name="ZU")
U_U = FNode([FExpr(Z_Z, Z_Z)], name="UU")
U_Z = FNode([FExpr(Z_Z, Z)], name="UZ")


ZZ_ZU = FNode([FExpr(Z, Z), FExpr(Z, U)], name="ZZ_ZU")
ZZ_UZ = FNode([FExpr(Z, Z), FExpr(U, Z)], name="ZZ_UZ")
ZZ_UU = FNode([FExpr(Z, Z), FExpr(U, U)], name="ZZ_UU")
ZU_ZZ = FNode([FExpr(Z, U), FExpr(Z, Z)], name="ZU_ZZ")
ZU_ZU = FNode([FExpr(Z, U), FExpr(U, U)], name="ZU_ZU")
ZU_UZ = FNode([FExpr(Z, U), FExpr(U, Z)], name="ZU_UZ")
ZU_UU = FNode([FExpr(Z, U), FExpr(U, U)], name="ZU_UU")
UZ_ZZ = FNode([FExpr(U, Z), FExpr(Z, Z)], name="UZ_ZZ")
UZ_UZ = FNode([FExpr(U, Z), FExpr(U, Z)], name="UZ_UZ")
UZ_UU = FNode([FExpr(U, Z), FExpr(U, U)], name="UZ_UU")
UU_ZZ = FNode([FExpr(U, U), FExpr(Z, Z)], name="UU_ZZ")
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

# Matrix-based behavior test runner
def run_behavior_matrix():
    results = []
    test_node_names = list(NAMED_NODES.keys())
    for name1 in test_node_names:
        for name2 in test_node_names:
            expr = FExpr(name1, name2)
            result = rewrite_edge(expr)
            tag = auto_behavior_tags(expr, result) if isinstance(result, list) else "no_match"
            results.append({
                "lhs": name1,
                "rhs": name2,
                "lhs_node": expr.left,
                "rhs_node": expr.right,
                "result": result,
                "tag": tag
            })
    return results

# Unit tests
class TestRewriteSystem(unittest.TestCase):

    def test_rule_Z_applied_to_expr(self):
        expr = FExpr(Z, Z_U)
        result = rewrite_edge(expr)
        self.assertEqual(result, [FExpr(Z, Z_U)])

    def test_rule_expr_applied_to_Z(self):
        expr = FExpr(Z_U, Z)
        result = rewrite_edge(expr)
        self.assertEqual(result, [FExpr(Z, U)])

    def test_rule_ZZ_applied_to_expr(self):
        expr = FExpr(Z_Z, Z_U)
        result = rewrite_edge(expr)
        self.assertEqual(result, [FExpr(Z, Z_Z)])

    def test_rule_expr_applied_to_ZZ(self):
        raise Exception("Not implemented")

    def test_boolean_and(self):
        false_val = FNode([FExpr(Z, Z)], name="false")
        true_val = FNode([FExpr(Z, U)], name="true")
        # if first arg is false, then anything returns false, 
        # if first arg is true, then second arg returns itself
        """
         # [FExpr(CF, Z)] => [FExpr(Z, Z)], # [FExpr(CF, U)] => [FExpr(Z, Z)]
         # CF = FNode([FExpr(Z, U)], name="CF")

        """
        constant_false = FNode([FExpr(Z, U)], name="CF")
        """
        # [FExpr(ID, Z_Z)] => [FExpr(Z, Z)], # [FExpr(ID, Z_U)] => [FExpr(Z, U)]
        # ID = FNode([FExpr(Z, Z)], name="ID")
        """
        id_fn = FNode([FExpr(Z, Z)], name="ID")
        """
        # ADD [Z, Z] => [Z, U]
        # ADD [Z, U] => [Z, Z]
        [U, Z] [Z, U] = > [U, U] => [Z, Z]
        [U, Z] [Z, Z] => [U, Z] => [Z, Z]
        [[Z, U], Z] [Z, Z] => [Z, U] [Z] => [Z, U]
        [[Z, U], Z] [Z, U] => [Z, U] [U] => [Z, Z]
        """
        
        A = FNode([FExpr(
            FNode([FExpr(Z, U)]),
            Z
        )], name="AND")
        and_res_1 = rewrite_edge(FExpr(A, false_val))
        print(and_res_1)
        print(constant_false)
        assert and_res_1 == constant_false
        and_res_2 = rewrite_edge(FExpr(A, true_val))
        assert and_res_2 == id_fn

    def test_boolean_or(self):
        raise Exception("Not implemented")


    def test_boolean_not(self):
        raise Exception("Not implemented")

    def test_boolean_xor(self):
        raise Exception("Not implemented")


    def test_pattern_replicator_rule(self):
        raise Exception("Not implemented")
        lhs = test_nodes["ZU_UZ"]
        rhs = FNode([(0, 3), (1, 3)])
        result = rewrite_edge(lhs, rhs)
        self.assertEqual(result, rhs)

    def test_duplication_rule(self):
        raise Exception("Not implemented")
        lhs = test_nodes["ZU_UU"]
        rhs = FNode([(0, 2), (1, 3)])
        result = rewrite_edge(lhs, rhs)
        self.assertEqual(result, [(0, 3), (1, 3)])

    def test_reduce_to_Z_rule(self):
        raise Exception("Not implemented")
        lhs = FNode([(0, 5), (1, 6)])
        rhs = FNode([(0, 5), (1, 6)])
        result = rewrite_edge(lhs, rhs)
        self.assertEqual(result, [])

    def test_behavior_matrix(self):
        results = run_behavior_matrix()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        pprint(results[:5])  # Show only the first few for brevity

