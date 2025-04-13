from hmac import new
from os import name
import re
from tkinter import E, N
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
        for i, edge in enumerate(self.edges):
            if edge != other.edges[i]:
                return False
        return True




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

        if not isinstance(right, FExpr):
            raise ValueError(f"Invalid argument: {right}")                    
        self.left = left
        self.right = right


    def __eq__(self, other) -> bool:
        if not isinstance(other, FExpr):
            return False
        equal = self.left == other.left and self.right == other.right
        return equal



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
U: FNode = FNode([FExpr(Z, Z)], name="U")

NAMED_EXPRS = {
    "U": FExpr(Z, Z),
}


# Rewrite rules
def rewrite_edge(edge: FExpr) -> List[FExpr]:
    if edge.left == Z:
        pass
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



ZU = FNode([FExpr("Z", "U")], name="ZU")
UU = FNode([FExpr("U", "U")], name="UU")
ZZ = FNode([FExpr("Z", "Z")], name="ZZ")
ZU_UZ = FNode([FExpr("Z", "U"), FExpr("U", "Z")], name="ZU_UZ")
ZU_UU = FNode([FExpr("Z", "U"), FExpr("U", "U")], name="ZU_UU")
UZ = FNode([FExpr("U", "Z")], name="UZ")
UUZU = FNode([FExpr("U", "U"), FExpr("Z", "U")], name="UUZU")
ZUZU = FNode([FExpr("Z", "U"), FExpr("U", "Z")], name="ZUZU")
ZZU = FNode([FExpr("Z", "Z"), FExpr("Z", "Z")], name="ZZU")
ZZZ = FNode([FExpr("Z", "Z"), FExpr("U", "Z")], name="ZZZ")
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
        expr = FExpr(Z, ZU)
        result = rewrite_edge(expr)
        self.assertEqual(result, [(0, 1)])

    def test_rule_expr_applied_to_Z(self):
        expr = FExpr(ZU, Z)
        result = rewrite_edge(expr)
        self.assertEqual(result, [(0, 0)])

    def test_rule_ZZ_applied_to_expr(self):
        expr = FExpr(ZZ, ZU)
        result = rewrite_edge(expr)
        self.assertEqual(result, [(0, 1)])

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

