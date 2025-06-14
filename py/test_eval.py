from ast import alias
from asyncio import Future
from hmac import new
from typing import Any, List, Tuple, Dict, Optional, Union, Self, final
import unittest
from pprint import pprint


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
type FExpr = Tuple[FNode, FNode]


events = []


class FNode:

    def __init__(self, args: List[FExpr], name: str | None = None):

        self.node_map: Dict[str, "FNode"] = {}
        self.alias_map: Dict[str, "FNode"] = {}

        self.edges: List[FExpr] = []
        self.name = name
        if name:
            if name in self.node_map:
                if self.node_map[name] != self:
                    raise ValueError(f"Node {name} already defined")
            self.node_map[name] = self
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

    def rewrite(self):
        """
        - (expr) -> (expr)
        """
        new_edges = []
        is_same = True
        for i, edge in enumerate(self.edges):
            if not isinstance(edge, tuple):
                print(self.edges)
                raise ValueError(f"Invalid argument: {edge}")
            res: List[FExpr] = edge[0].rewrite_from_input(edge[1])
            if len(res) != 1 or res[0] != edge:
                is_same = False
                new_edges.extend(res)
        if is_same:
            return self
        else:
            new_node = FNode(new_edges, name=self.name)
            final_node = new_node.rewrite()
            return final_node

    # Rewrite rules
    def rewrite_from_input(self, other: "FNode") -> List[FExpr]:
        if not other:
            raise ValueError(f"Invalid argument: {edge}")
        if self == Z:
            return [edge]
        if other == Z:
            return self.edges
        new_edges = []
        for l_edge in self.edges:
            if l_edge.right == other:
                # print("here2", l_edge.left, l_edge, edge.right)
                new_edges.append(FExpr(l_edge.left, Z))
            else:
                for r_edge in other.edges:
                    # print("here2", l_edge, r_edge)
                    if l_edge[0].match_input(r_edge[0]):
                        new_edges.append((l_edge[0], r_edge[1]))

        return new_edges

    def match_input(self, target: "FNode"):
        if self == Z:
            return True
        if self == target:
            return True
        for i, p_edge in enumerate(self.edges):
            has_edge_match = any(
                [
                    p_edge[0].match_input(t_edge[1])
                    and p_edge[1].match_input(t_edge[1])
                    for t_edge in target.edges
                ]
            )
            return has_edge_match
        return True

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

        - how about arguments?
            - type checking?
            - consumable resources?
            - come in as default arguments?
            - channel fulfils role?  Role is type
            - cahnnel on left:
                - right argument is new task
            - channel on right:
                - left
            - current node is responsible for:
                - type checking
                    - ask each term in tree if type matches
                - resource checking
                    - ask each term in tree if resource matches




        """

    def set_input(self, input: Self):
        self.input = input
        return self

    def trigger_output_event(self):
        pass

    async def rewrite_worker(self, output: Self):
        # do rewrites and at the end, trigger output event
        pass

    def evaluate(self, other: Self):
        """
        - if other is a node with bindings, then transfer bindings
        - if node is pure,
        """
        pass

    def __hash__(self) -> int:
        tuple_based = hash(tuple(sorted(self.edges)))
        return tuple_based

    def from_yaml(self, yaml_str: str):
        """
        - parse yaml
        - create nodes
        - create edges
        - return node
        """
        pass

    def to_yaml(self):
        """
        - convert node to yaml
        - return yaml string
        """
        pass

    def add_alias(self, alias: str):
        pass

    def add_expr(self, task: str):
        """
        -
        """
        pass

    def send_message(self, reply_channel: "FNode", arg: "FNode"):
        pass

    def register_sender(self, sender: str):
        """
        - register sender
        - return sender
        """
        pass

    def run():
        """
        - receive on http:
            - base url = cid or uuid
            - capabilities = ???
                - registered per node? (right side of edges?)
            -
        - return node
        """
        pass


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
