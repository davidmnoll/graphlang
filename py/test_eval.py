from typing import List, Tuple, Dict, Optional
import unittest
from pprint import pprint

# Core types
NodeId = int
Expr = Tuple[NodeId, NodeId]
Node = List[Expr]

# Primitive nodes
Z: Node = []
U: Node = [(0, 0)]






# Rewrite rules
def match_and_rewrite(lhs: Node, rhs: Node) -> Optional[Node]:
    if lhs == [] and len(rhs) == 1:
        return [(0, rhs[0][1])]
    if rhs == [] and len(lhs) == 1:
        return [(lhs[0][0], 0)]
    if lhs == [(0, 0)] and len(rhs) == 1:
        return [(0, rhs[0][1])]
    if lhs == [(0, 0), (1, 0)] and len(rhs) == 1 and rhs[0][0] == 0:
        return [(0, rhs[0][1]), (1, rhs[0][1])]
    if lhs == [(0, 0), (1, 0)] and len(rhs) == 2 and rhs[0][0] == 0 and rhs[1][0] == 1 and rhs[0][1] == rhs[1][1]:
        return rhs
    if lhs == [(0, 1), (1, 1)] and len(rhs) == 2 and rhs[0][0] == 0 and rhs[1][0] == 1:
        return [(0, rhs[1][1]), (1, rhs[1][1])]
    if lhs == rhs and len(lhs) == 2 and lhs[0][0] == 0 and lhs[1][0] == 1:
        return []
    return None

# Z-termination checker
def terminates_in_z(exprs: Node, side: str, nodes: Dict[int, Node]) -> bool:
    visited = set()
    def traverse(nid: NodeId) -> bool:
        if nid == 0:
            return True
        if nid in visited or nid not in nodes:
            return False
        visited.add(nid)
        for l, r in nodes[nid]:
            if traverse(l) or traverse(r):
                return True
        return False
    for l, r in exprs:
        nid = l if side == "left" else r
        if not traverse(nid):
            return False
    return True

# Rewrite with causal constraint unless bypassed
def recursive_match_and_rewrite(lhs: Node, rhs: Node, nodes: Dict[int, Node], bypass=False) -> Optional[Node]:
    if bypass or (terminates_in_z(lhs, "right", nodes) and not terminates_in_z(rhs, "left", nodes)):
        return match_and_rewrite(lhs, rhs)
    return None






# Test node definitions
test_nodes: Dict[str, Node] = {
    "Z": Z,
    "U": U,
    "ZU": [(0, 1)],
    "UZ": [(1, 0)],
    "UU": [(1, 1)],
    "ZUZU": [(0, 1), (1, 0)],
    "UUZU": [(1, 1), (0, 1)],
    "ZZ": [(0, 0)],
    "ZU_UZ": [(0, 1), (1, 0)],
    "ZU_UU": [(0, 1), (1, 1)],
}

# Node registry for recursive traversal
nodes: Dict[int, Node] = {i: n for i, n in enumerate([Z, U] + list(test_nodes.values())[2:], start=0)}


# Behavior tagging
def auto_behavior_tags(lhs: Node, rhs: Node, result: Node) -> str:
    if result == []:
        return "reduces_to_Z"
    if result == [(0, 0)]:
        return "reduces_to_U"
    if result == lhs:
        return "id_like"
    if result == rhs:
        return "const_like"
    if sorted(result) == sorted(rhs) and lhs != rhs:
        return "pattern_replicator"
    if all(expr[1] == result[0][1] for expr in result):
        return "possible_duplication"
    return "unclassified"

# Matrix-based behavior test runner
def run_behavior_matrix():
    results = []
    test_node_names = list(test_nodes.keys())
    for name1 in test_node_names:
        for name2 in test_node_names:
            lhs = test_nodes[name1]
            rhs = test_nodes[name2]
            result = recursive_match_and_rewrite(lhs, rhs, nodes)
            tag = auto_behavior_tags(lhs, rhs, result) if isinstance(result, list) else "no_match"
            results.append({
                "lhs": name1,
                "rhs": name2,
                "lhs_node": lhs,
                "rhs_node": rhs,
                "result": result,
                "tag": tag
            })
    return results

# Unit tests
class TestRewriteSystem(unittest.TestCase):

    def test_rule_Z_applied_to_expr(self):
        lhs = test_nodes["Z"]
        rhs = test_nodes["ZU"]
        result = recursive_match_and_rewrite(lhs, rhs, nodes, bypass=True)
        self.assertEqual(result, [(0, 1)])

    def test_rule_expr_applied_to_Z(self):
        lhs = test_nodes["ZU"]
        rhs = test_nodes["Z"]
        result = recursive_match_and_rewrite(lhs, rhs, nodes, bypass=True)
        self.assertEqual(result, [(0, 0)])

    def test_rule_ZZ_applied_to_expr(self):
        lhs = test_nodes["ZZ"]
        rhs = test_nodes["ZU"]
        result = recursive_match_and_rewrite(lhs, rhs, nodes, bypass=True)
        self.assertEqual(result, [(0, 1)])

    def test_pattern_replicator_rule(self):
        lhs = test_nodes["ZU_UZ"]
        rhs = [(0, 3), (1, 3)]
        result = match_and_rewrite(lhs, rhs)
        self.assertEqual(result, rhs)

    def test_duplication_rule(self):
        lhs = test_nodes["ZU_UU"]
        rhs = [(0, 2), (1, 3)]
        result = match_and_rewrite(lhs, rhs)
        self.assertEqual(result, [(0, 3), (1, 3)])

    def test_reduce_to_Z_rule(self):
        lhs = [(0, 5), (1, 6)]
        rhs = [(0, 5), (1, 6)]
        result = match_and_rewrite(lhs, rhs)
        self.assertEqual(result, [])

    def test_behavior_matrix(self):
        results = run_behavior_matrix()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        pprint(results[:5])  # Show only the first few for brevity

