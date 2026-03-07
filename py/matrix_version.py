from re import M
from typing import List, Tuple
import math
from anytree import Node, RenderTree
from typing import Union

import matrix_viz


def hilbert_xy_to_d(n, x, y):
    """Convert (x, y) coordinates to Hilbert curve distance."""
    d = 0
    s = n // 2
    while s > 0:
        rx = int((x & s) > 0)
        ry = int((y & s) > 0)
        d += s * s * ((3 * rx) ^ ry)
        x, y = hilbert_rot(s, x, y, rx, ry)
        s //= 2
    return d


def hilbert_d_to_xy(n, d):
    """Convert Hilbert curve distance to (x, y) coordinates."""
    x = y = 0
    s = 1
    while s < n:
        rx = int((d // 2) & 1)
        ry = int((d ^ rx) & 1)
        x, y = hilbert_rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        d //= 4
        s *= 2
    return x, y


def hilbert_rot(n, x, y, rx, ry):
    """Rotate/flip quadrant appropriately for Hilbert curve."""
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        x, y = y, x
    return x, y


# def part1by1(x):
#     """Spread the bits of x so that there is one zero bit between each of the original bits."""
#     x &= 0xFFFF
#     x = (x | (x << 8)) & 0x00FF00FF
#     x = (x | (x << 4)) & 0x0F0F0F0F
#     x = (x | (x << 2)) & 0x33333333
#     x = (x | (x << 1)) & 0x55555555
#     return x


# def morton_flipped(i, j):
#     """Your version: interleave column (j) first, then row (i)"""
#     return part1by1(j) | (part1by1(i) << 1)


# def morton_index(row, col):
#     return part1by1(row) | (part1by1(col) << 1)


# def compact1by1(x):
#     """Extract every other bit starting from LSB (reverse of part1by1)"""
#     x &= 0x55555555
#     x = (x | (x >> 1)) & 0x33333333
#     x = (x | (x >> 2)) & 0x0F0F0F0F
#     x = (x | (x >> 4)) & 0x00FF00FF
#     x = (x | (x >> 8)) & 0x0000FFFF
#     return x


# def inverse_morton(index: int) -> Tuple[int, int]:
#     x = compact1by1(index)
#     y = compact1by1(index >> 1)
#     return x, y


def get_matrix_from_int_hilbert(n: int) -> List[List[bool]]:
    if n == 0:
        return []

    num_bits = n.bit_length()
    sqr_ceil = math.ceil(math.sqrt(num_bits))
    dim = 1 if sqr_ceil < 1 else 1 << (sqr_ceil - 1).bit_length()
    total_bits = dim * dim

    bitstr = bin(n)[2:].zfill(total_bits)[::-1]  # LSB first
    matrix = [[False for _ in range(dim)] for _ in range(dim)]

    for i in range(dim):
        for j in range(dim):
            index = hilbert_xy_to_d(dim, i, j)
            if index < len(bitstr):
                matrix[i][j] = bitstr[index] == "1"

    return matrix


# def get_matrix_from_int_morton(n: int) -> List[List[bool]]:
#     if n == 0:
#         return []

#     num_bits = n.bit_length()
#     sqr_ceil = math.ceil(math.sqrt(num_bits))
#     dim = 1 if sqr_ceil < 1 else 1 << (sqr_ceil - 1).bit_length()
#     total_bits = dim * dim

#     bitstr = bin(n)[2:].zfill(total_bits)[::-1]  # LSB first
#     matrix = [[False for _ in range(dim)] for _ in range(dim)]

#     for i in range(dim):
#         for j in range(dim):
#             index = morton_index(i, j)
#             if index < len(bitstr):
#                 matrix[i][j] = bitstr[index] == "1"

#     return matrix


# def get_matrix_from_int_flipped_morton(n: int) -> List[List[bool]]:
#     if n == 0:
#         return []

#     num_bits = n.bit_length()
#     sqr_ceil = math.ceil(math.sqrt(num_bits))
#     dim = 1 << (sqr_ceil - 1).bit_length()
#     total_bits = dim * dim
#     bitstr = bin(n)[2:].zfill(total_bits)[::-1]  # LSB-first

#     matrix = [[False for _ in range(dim)] for _ in range(dim)]
#     for i in range(dim):
#         for j in range(dim):
#             index = morton_flipped(i, j)
#             if index < total_bits:
#                 matrix[i][j] = bitstr[index] == "1"
#     return matrix


# def get_matrix_from_int_hybrid_morton(n: int) -> List[List[bool]]:
#     if n == 0:
#         return []

#     num_bits = n.bit_length()
#     sqr_ceil = math.ceil(math.sqrt(num_bits))
#     dim = 1 << (sqr_ceil - 1).bit_length()
#     total_bits = dim * dim
#     bitstr = bin(n)[2:].zfill(total_bits)[::-1]  # LSB-first

#     matrix = [[False for _ in range(dim)] for _ in range(dim)]
#     for i in range(dim):
#         for j in range(dim):
#             if i < j:  # above diagonal: use flipped Morton
#                 index = morton_flipped(i, j)
#             else:  # diagonal & below: use regular Morton
#                 index = morton_index(i, j)
#             if index < total_bits:
#                 matrix[i][j] = bitstr[index] == "1"
#     return matrix


def get_matrix_from_int(n: int) -> List[List[bool]]:

    if n == 0:
        return []

    num_bits = n.bit_length()
    sqr_ceil = math.ceil(math.sqrt(num_bits))
    dim = 1 if sqr_ceil < 1 else 1 << (sqr_ceil - 1).bit_length()
    # level = math.sqrt(math.ceil(math.log2(n)))
    total_bits = dim * dim

    bitstr = bin(n)[2:].zfill(total_bits)

    if not dim.is_integer():
        print(
            f"Matrix dimension for {n}: {dim}, Bit string length: {n.bit_length()} - ({bitstr})"
        )
        raise ValueError("Matrix dimension not valid.")
    matrix = []
    for i, val in enumerate(bitstr[::-1]):
        if i % dim == 0:
            matrix.append([])
        matrix[i // dim].append(bool(int(val)))
    return matrix


def matrix_to_int_hilbert(matrix: List[List[bool]]) -> int:
    if not matrix:
        return 0

    dim = len(matrix)
    bits = ["0"] * (dim * dim)
    for i in range(dim):
        for j in range(dim):
            index = hilbert_xy_to_d(dim, i, j)
            bits[index] = "1" if matrix[i][j] else "0"

    bits.reverse()  # LSB-last
    return int("".join(bits), 2)


# def matrix_to_int_flipped_morton(matrix: List[List[bool]]) -> int:
#     if not matrix:
#         return 0

#     dim = len(matrix)
#     bits = ["0"] * (dim * dim)
#     for i in range(dim):
#         for j in range(dim):
#             index = morton_flipped(i, j)
#             bits[index] = "1" if matrix[i][j] else "0"

#     bits.reverse()  # LSB-last
#     return int("".join(bits), 2)


# def matrix_to_int_hybrid_morton(matrix: List[List[bool]]) -> int:
#     if not matrix:
#         return 0

#     dim = len(matrix)
#     bits = ["0"] * (dim * dim)

#     for i in range(dim):
#         for j in range(dim):
#             if i < j:
#                 index = morton_flipped(i, j)
#             else:
#                 index = morton_index(i, j)
#             bits[index] = "1" if matrix[i][j] else "0"

#     bits.reverse()  # LSB-last
#     return int("".join(bits), 2)


class MatrixGraph:

    def __init__(self, n: int):
        # matrix = get_matrix_from_int_flipped_morton(n)
        # matrix = get_matrix_from_int_morton(n)
        matrix = get_matrix_from_int_flipped_morton(n)
        self.entries = entries_from_matrix(matrix)
        # print(
        #     f"MatrixGraph for {n} initialized with entries: {self.entries} and matrix: {matrix}"
        # )

    def __repr__(self):
        repr_str = ""
        repr_str += (
            f"MatrixGraph({self.to_int()}) {"-" if len(self.entries) else ""} \n"
        )
        for src, dst in self.entries:
            repr_str += f"{src.to_int()} -> {dst.to_int()}, \n"
        return repr_str

    def to_matrix(self) -> List[List[bool]]:
        if not self.entries:
            return []

        max_index = max(max(e[0].to_int(), e[1].to_int()) for e in self.entries)
        dim = 1 << (max_index.bit_length())
        matrix = [[False for _ in range(dim)] for _ in range(dim)]

        for src, dst in self.entries:
            i, j = src.to_int(), dst.to_int()
            matrix[i][j] = True
        return matrix

    # def to_int(self) -> int:
    #     matrix = self.to_matrix()
    #     if not matrix:
    #         return 0

    #     dim = len(matrix)
    #     flat_bits = ["0"] * (dim * dim)

    #     for i in range(dim):
    #         for j in range(dim):
    #             morton = morton_index(i, j)
    #             flat_bits[morton] = "1" if matrix[i][j] else "0"

    #     flat_bits.reverse()  # LSB last
    #     return int("".join(flat_bits), 2)

    def to_int(self) -> int:
        matrix = self.to_matrix()
        return_int = matrix_to_int_flipped_morton(matrix)
        return return_int

    def to_anytree(self, label: Union[str, None] = None) -> Node:
        """
        Recursively convert a MatrixGraph into an anytree.Node.
        If the graph is a leaf, return a node with its index.
        """
        name = f"{label:}{self.to_int()}" if label else f"{self.to_int()}"
        root = Node(name)

        for i, (src, dst) in enumerate(self.entries):
            edge_label = f"{src.to_int()} → {dst.to_int()}"
            # Recursively attach the destination as a child
            child1 = src.to_anytree(f"L{i}:")
            child2 = dst.to_anytree(f"R{i}:")
            child1.parent = root
            child2.parent = root
        return root

    def print_anytree(self):
        tree_root = self.to_anytree()
        for pre, _, node in RenderTree(tree_root):
            print(f"{pre}{node.name}")


def entries_from_matrix(
    matrix: List[List[bool]],
) -> List[Tuple[MatrixGraph, MatrixGraph]]:
    entries = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                entries.append((MatrixGraph(i), MatrixGraph(j)))
    return entries


if __name__ == "__main__":

    for i in [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
        for j, k in enumerate(range(i, 520 * i, i)):
            mg = MatrixGraph(k)
            dim = len(mg.to_matrix())
            print(
                f"n={i}, j={j} k={k} entries={[ (e[0].to_int(), e[1].to_int()) for e in mg.entries ]}"
            )
            mg_int = mg.to_int()
            assert mg.to_int() == k, f"mg_int for {i} is {mg.to_int()}"
        print("===============================")
        # matrix_viz.visualize_matrixgraph_colored(mg, f"matrix_viz-{i}")

    # for i in range(258):
    #     m = MatrixGraph(i)
    #     print(f"m{i}", m)
    #     assert m.to_int() == i

    # m3 = MatrixGraph(3)
    # m5 = MatrixGraph(5)
    # m7 = MatrixGraph(7)
    # m11 = MatrixGraph(11)

    # print("m3", m3)
    # print("m5", m5)
    # print("m7", m7)
    # print("m11", m11)

    # m3 = MatrixGraph(3)
    # print(m3)

    # m16 = MatrixGraph(16).to_int()
    # print(f"MatrixGraph(16) to int: {m16}")

    # assert m16.to_matrix() == [
    #     [0, 0, 1, 0],
    #     [0, 0, 0, 0],
    #     [0, 0, 0, 0],
    #     [0, 0, 0, 0],
    # ]

    # assert MatrixGraph(16).to_int() == 16
    # assert MatrixGraph(17).to_int() == 17

    # print(get_matrix_from_int_flipped_morton(0))  # Should return 0
    # assert get_matrix_from_int_flipped_morton(0) == []
    # print(get_matrix_from_int_flipped_morton(1))  # Should return [[1]]
    # assert get_matrix_from_int_flipped_morton(1) == [[1]]
    # print(get_matrix_from_int_flipped_morton(2))  # Should return [[0, 1], [0, 0]]
    # assert get_matrix_from_int_flipped_morton(2) == [[0, 1], [0, 0]]
    # assert get_matrix_from_int_flipped_morton(3) == [[1, 1], [0, 0]]

    # assert get_matrix_from_int_flipped_morton(14) == [[0, 1], [1, 1]]
    # assert get_matrix_from_int_flipped_morton(15) == [[1, 1], [1, 1]]

    # assert get_matrix_from_int(4) == [[0, 0], [1, 0]]
    # assert get_matrix_from_int(5) == [[1, 0], [1, 0]]
    # assert get_matrix_from_int(6) == [[0, 1], [1, 0]]
    # assert get_matrix_from_int(7) == [[1, 1], [1, 0]]
    # assert get_matrix_from_int(8) == [[0, 0], [0, 1]]
    # assert get_matrix_from_int(9) == [[1, 0], [0, 1]]
    # assert get_matrix_from_int(10) == [[0, 1], [0, 1]]
    # assert get_matrix_from_int(11) == [[1, 1], [0, 1]]
    # assert get_matrix_from_int(12) == [[0, 0], [1, 1]]
    # assert get_matrix_from_int(13) == [[1, 0], [1, 1]]
