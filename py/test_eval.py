from asyncio import Future
from hmac import new
from typing import Any, List, Tuple, Dict, Optional, Union, Self, final
import unittest
from pprint import pprint


"""
- Forward communication: 
    - for each subscriber, send message
    - upon subscription, passes key to 

"""

NAMED_NODES: Dict[str, "FNode"] = {}
NAMED_EXPRS: Dict[str, "FExpr"] = {}


class FNode:

    name: str | None = None
    inputs: List[Self] = []
    subscriber_addrs: List[str] = []

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

    def subscribe_events(self, sender_addr: str):
        """
        - aggregate list of channel addrs from tree
        - for each one,
            - if content address, get content
            - if content local, substitute directly
            - else send request for content to events channel?
                - message not encrypted, contains my pub key?
                - signed with my private key?
            - if pub key get pub key, decode data
        - substitute data into channel instance
        - if no more channels subscribed, then trigger output event
            - one for each subscriber?  / encrypted?
                - how would subscribers be known?
                - signed wiht private key & giving pub key?



        """

    def set_input(self, input: Self):
        self.input = input
        return self

    def trigger_output_event(self):
        pass

    async def rewrite_worker(self, output: Self):
        # do rewrites and at the end, trigger output event
        pass


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
        constant_false = FNode([FExpr(U, Z)])
        id_fn = U

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

    def test_boolean_or(self):
        false_val = FNode([FExpr(Z, Z)])
        true_val = FNode([FExpr(Z, U)])
        # if first arg is true, then anything returns true, (constant true)
        # if first arg is false, then second arg returns itself (id)
        constant_true = FNode([FExpr(FNode([FExpr(Z_U, Z)]), Z)])
        id_fn = FNode([FExpr(Z, Z)])

        O = FNode([FExpr(constant_true, true_val), FExpr(id_fn, false_val)])
        and_res_1 = rewrite_edge(rewrite_edge(FExpr(O, false_val))[0])
        print(FNode(and_res_1), id_fn)
        assert FNode(and_res_1) == id_fn
        and_res_2 = rewrite_edge(rewrite_edge(FExpr(O, true_val))[0])
        print(and_res_2)
        print(constant_true)
        assert FNode(and_res_2) == constant_true

    def test_k_combinator(self):
        """
        X would be a channel which is subscribed to the outer input.



        """
        K_comb = FNode([FExpr(FNode([FExpr(X, Z)]), Z)])

    @unittest.skip("Skipping test for now")
    def test_s_combinator(self):
        raise NotImplementedError("S combinator test not implemented yet")

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
