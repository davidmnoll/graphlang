from anytree import Node
from anytree.exporter import DotExporter
from graphviz import Digraph
import os
import os

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os
from graphviz import Digraph
from matrix_version import (
    MatrixGraph,
)  # Make sure matrix_version.py is in your Python path or working directory


def export_matrixgraph_graphviz(g, filename="tree"):
    dot_filename = f"artifacts/{filename}.dot"
    png_filename = f"artifacts/{filename}.png"

    with open(dot_filename, "w") as f:
        f.write("digraph G {\n")
        f.write("  rankdir=RL;\n")  # Right-to-left layout

        seen = set()

        for src, dst in g.entries:
            s = f"n{src.to_int()}"
            d = f"n{dst.to_int()}"

            # Declare nodes
            if s not in seen:
                f.write(f'  {s} [label="{src.to_int()}"];\n')
                seen.add(s)
            if d not in seen:
                f.write(f'  {d} [label="{dst.to_int()}"];\n')
                seen.add(d)

            # Arrow direction (source → destination)
            f.write(f"  {s} -> {d};\n")

        f.write("}\n")

    os.system(f"dot -Tpng {dot_filename} -o {png_filename}")
    print(f"Saved Graphviz right-to-left tree as: {png_filename}")


def draw_asymmetric_tree(graph, filename="tree", outdir="."):
    edges = [(src.to_int(), dst.to_int()) for src, dst in graph.entries]
    if not edges:
        print("Empty graph.")
        return

    # Build adjacency list
    from collections import defaultdict

    children = defaultdict(list)
    for src, dst in edges:
        children[src].append(dst)

    dot = Digraph(engine="neato")
    dot.attr(overlap="false")
    dot.attr(splines="true")
    dot.attr("node", shape="circle")

    seen = set()
    positions = {}

    def layout(node, x=0, y=0, direction=1):
        if node in seen:
            return
        seen.add(node)
        pos_str = f"{x},{-y}!"
        dot.node(str(node), str(node), pos=pos_str)
        positions[node] = (x, y)

        if node not in children:
            return

        offset = 1
        for child in sorted(children[node]):
            child_dir = -1 if child < node else 1
            next_x = x + child_dir * offset
            next_y = y + 1
            layout(child, next_x, next_y, child_dir)
            dot.edge(str(node), str(child))
            offset += 2

    # Choose a root — default to the lowest-numbered source
    root = min(src for src, _ in edges)
    layout(root)

    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, filename)
    dot.render(outfile, format="png", cleanup=True)
    print(f"Saved asymmetric tree to: {outfile}.png")


def draw_ltr_trees(entries, outdir="trees", show=True, save=True):
    os.makedirs(outdir, exist_ok=True)

    for i, (src, dst) in enumerate(entries):
        root = Node(f"root_{i}")
        src_node = Node(f"L:{src.to_int()}", parent=root)
        dst_node = Node(f"R:{dst.to_int()}", parent=root)

        # Print to terminal
        if show:
            print(f"Tree {i} - ({src.to_int()} -> {dst.to_int()})")
            for pre, _, node in RenderTree(root):
                print(f"{pre}{node.name}")
            print()

        # Save as image using Graphviz
        if save:
            dot_path = os.path.join(outdir, f"tree_{i}.dot")
            img_path = os.path.join(outdir, f"tree_{i}.png")

            DotExporter(root).to_dotfile(dot_path)
            os.system(f"dot -Tpng {dot_path} -o {img_path}")
            print(f"Saved: {img_path}")


def visualize_matrix_graph_spine(
    graph: MatrixGraph, filename: str = "matrix_spine_graph"
) -> None:
    """
    Visualize a MatrixGraph instance with spine layout. Each entry creates a central node
    with left and right nodes pointing outward (left and right respectively).

    Parameters:
        graph (MatrixGraph): A MatrixGraph object.
        filename (str): Output file name without extension.
    """
    dot = Digraph(format="png")
    dot.attr(rankdir="LR", layout="dot")

    for idx, (left_node, right_node) in enumerate(graph.entries):
        center_id = f"entry_{idx}"
        dot.node(
            center_id, label=center_id, shape="box", style="filled", fillcolor="gray95"
        )

        # Create left and right nodes (values from MatrixGraph.to_int())
        left_val = left_node.to_int()
        right_val = right_node.to_int()

        left_id = f"{center_id}_L_{left_val}"
        right_id = f"{center_id}_R_{right_val}"

        dot.node(left_id, label=str(left_val), style="filled", fillcolor="lightblue")
        dot.edge(center_id, left_id)

        dot.node(right_id, label=str(right_val), style="filled", fillcolor="lightgreen")
        dot.edge(center_id, right_id)

    dot.render(filename, cleanup=True)
    dot.view(filename)
