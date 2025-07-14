from typing import List, Tuple, Union
import math
from anytree import Node, RenderTree

import matrix_viz
from matrix_base import MatrixBase


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


def get_matrix_from_int_hilbert(n: int) -> List[List[bool]]:
    if n == 0:
        return []

    num_bits = n.bit_length()
    sqr_ceil = math.ceil(math.sqrt(num_bits))
    dim = 1 if sqr_ceil < 1 else 1 << (sqr_ceil - 1).bit_length()
    total_bits = dim * dim

    bitstr = bin(n)[2:].zfill(total_bits)[::-1]  # LSB first, so bit 0 is at index 0
    matrix = [[False for _ in range(dim)] for _ in range(dim)]

    # For each bit position in the number
    for bit_pos in range(len(bitstr)):
        if bit_pos < total_bits:
            # Find the Hilbert position for this bit
            hilbert_pos = bit_pos
            # Convert Hilbert position to (x,y) coordinates
            x, y = hilbert_d_to_xy(dim, hilbert_pos)
            # Place the bit value at those coordinates
            matrix[x][y] = bitstr[bit_pos] == "1"

    return matrix


def matrix_to_int_hilbert(matrix: List[List[bool]]) -> int:
    if not matrix:
        return 0

    dim = len(matrix)
    bits = ["0"] * (dim * dim)
    
    # For each position in the matrix
    for i in range(dim):
        for j in range(dim):
            # Convert (x,y) coordinates to Hilbert position
            hilbert_pos = hilbert_xy_to_d(dim, i, j)
            # This Hilbert position corresponds to bit position hilbert_pos
            if hilbert_pos < len(bits):
                bits[hilbert_pos] = "1" if matrix[i][j] else "0"

    bits.reverse()  # LSB-last for integer conversion
    return int("".join(bits), 2)


class MatrixHilbert(MatrixBase):

    def get_matrix_from_int(self, n: int) -> List[List[bool]]:
        return get_matrix_from_int_hilbert(n)

    def matrix_to_int(self, matrix: List[List[bool]]) -> int:
        return matrix_to_int_hilbert(matrix)


