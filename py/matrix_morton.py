from typing import List, Tuple, Union
import math
from anytree import Node, RenderTree

from .viz import matrix_viz
from matrix_base import MatrixBase


def part1by1(x):
    """Spread the bits of x so that there is one zero bit between each of the original bits."""
    x &= 0xFFFF
    x = (x | (x << 8)) & 0x00FF00FF
    x = (x | (x << 4)) & 0x0F0F0F0F
    x = (x | (x << 2)) & 0x33333333
    x = (x | (x << 1)) & 0x55555555
    return x


def morton_flipped(i, j):
    """Your version: interleave column (j) first, then row (i)"""
    return part1by1(j) | (part1by1(i) << 1)


def morton_index(row, col):
    return part1by1(row) | (part1by1(col) << 1)


def compact1by1(x):
    """Extract every other bit starting from LSB (reverse of part1by1)"""
    x &= 0x55555555
    x = (x | (x >> 1)) & 0x33333333
    x = (x | (x >> 2)) & 0x0F0F0F0F
    x = (x | (x >> 4)) & 0x00FF00FF
    x = (x | (x >> 8)) & 0x0000FFFF
    return x


def inverse_morton(index: int) -> Tuple[int, int]:
    x = compact1by1(index)
    y = compact1by1(index >> 1)
    return x, y


def get_matrix_from_int_morton(n: int) -> List[List[bool]]:
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
            index = morton_index(i, j)
            if index < len(bitstr):
                matrix[i][j] = bitstr[index] == "1"

    return matrix


def get_matrix_from_int_flipped_morton(n: int) -> List[List[bool]]:
    if n == 0:
        return []

    num_bits = n.bit_length()
    sqr_ceil = math.ceil(math.sqrt(num_bits))
    dim = 1 << (sqr_ceil - 1).bit_length()
    total_bits = dim * dim
    bitstr = bin(n)[2:].zfill(total_bits)[::-1]  # LSB-first

    matrix = [[False for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            index = morton_flipped(i, j)
            if index < total_bits:
                matrix[i][j] = bitstr[index] == "1"
    return matrix


def get_matrix_from_int_hybrid_morton(n: int) -> List[List[bool]]:
    if n == 0:
        return []

    num_bits = n.bit_length()
    sqr_ceil = math.ceil(math.sqrt(num_bits))
    dim = 1 << (sqr_ceil - 1).bit_length()
    total_bits = dim * dim
    bitstr = bin(n)[2:].zfill(total_bits)[::-1]  # LSB-first

    matrix = [[False for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for j in range(dim):
            if i < j:  # above diagonal: use flipped Morton
                index = morton_flipped(i, j)
            else:  # diagonal & below: use regular Morton
                index = morton_index(i, j)
            if index < total_bits:
                matrix[i][j] = bitstr[index] == "1"
    return matrix


def matrix_to_int_flipped_morton(matrix: List[List[bool]]) -> int:
    if not matrix:
        return 0

    dim = len(matrix)
    bits = ["0"] * (dim * dim)
    for i in range(dim):
        for j in range(dim):
            index = morton_flipped(i, j)
            bits[index] = "1" if matrix[i][j] else "0"

    bits.reverse()  # LSB-last
    return int("".join(bits), 2)


def matrix_to_int_hybrid_morton(matrix: List[List[bool]]) -> int:
    if not matrix:
        return 0

    dim = len(matrix)
    bits = ["0"] * (dim * dim)

    for i in range(dim):
        for j in range(dim):
            if i < j:
                index = morton_flipped(i, j)
            else:
                index = morton_index(i, j)
            bits[index] = "1" if matrix[i][j] else "0"

    bits.reverse()  # LSB-last
    return int("".join(bits), 2)


class MatrixMorton(MatrixBase):

    def get_matrix_from_int(self, n: int) -> List[List[bool]]:
        return get_matrix_from_int_flipped_morton(n)

    def matrix_to_int(self, matrix: List[List[bool]]) -> int:
        return matrix_to_int_flipped_morton(matrix)
