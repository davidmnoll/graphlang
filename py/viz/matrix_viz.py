import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def visualize_matrixgraph_colored(graph, save_name=""):
    entries = graph.entries
    all_nodes = set()
    for src, dst in entries:
        all_nodes.add(src.to_int())
        all_nodes.add(dst.to_int())

    dim = 1 << (max(all_nodes).bit_length())
    adj_matrix = np.zeros((dim, dim), dtype=int)
    depths = {}  # depth by destination

    def dfs(node, depth):
        if node.to_int() in depths:
            return
        depths[node.to_int()] = depth
        for s, d in node.entries:
            if s.to_int() == node.to_int():
                dfs(d, depth + 1)

    dfs(graph, 0)

    color_matrix = np.zeros((dim, dim, 3))  # RGB
    for src, dst in entries:
        i, j = src.to_int(), dst.to_int()
        adj_matrix[i, j] = 1
        depth = depths.get(dst.to_int(), 0)
        t = min(depth / 5, 1.0)
        if dst.to_int() > src.to_int():  # right branch
            color = (0, 1 - t, t)  # blue -> green
        else:  # left branch
            color = (1, t, 0)  # red -> orange
        color_matrix[i, j] = color

    fig, ax = plt.subplots()
    ax.imshow(color_matrix, interpolation="none")
    ax.set_xticks(np.arange(-0.5, dim, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, dim, 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)
    ax.set_xticks([])
    ax.set_yticks([])

    for i in range(dim):
        for j in range(dim):
            if adj_matrix[i, j]:
                ax.text(
                    j,
                    i,
                    f"{depths.get(j, 0)}",
                    va="center",
                    ha="center",
                    color="white",
                    fontsize=8,
                )

    ax.set_title(f"MatrixGraph({graph.to_int()}) Colored Grid (by Branch & Depth)")
    plt.show()
    if save_name:
        plt.savefig(f"./py/artifacts/{save_name}.png")
    else:
        plt.tight_layout()
