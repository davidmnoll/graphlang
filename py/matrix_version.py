from typing import List
import math


def int_to_matrix_triangle(n: int) -> List[List[bool]]:
    bits = get_bits(n)
    total_bits = len(bits)

    # Solve: k such that k*(k+1)/2 >= total_bits
    k = 0
    while (k * (k + 1)) // 2 < total_bits:
        k += 1

    needed_bits = (k * (k + 1)) // 2
    bits = [0] * (needed_bits - total_bits) + bits
    bits.reverse()  # make bit 0 map to (0,0)

    triangle = []
    index = 0
    for row in range(k):
        row_len = k - row  # top-heavy triangle
        triangle.append([bool(bits[index + i]) for i in range(row_len)])
        index += row_len

    return triangle


def int_to_coordinate(n: int) -> List[List[bool]]:
    bits = get_bits(n)
    num_bits = len(bits)

    coords = [deinterleave_right_first(i) for i in range(num_bits)]
    max_row = max(r for r, _ in coords)
    max_col = max(c for _, c in coords)

    matr = [[False for _ in range(max_col + 1)] for _ in range(max_row + 1)]

    for i, bit in enumerate(bits[::-1]):  # LSB first
        row, col = deinterleave_right_first(i)
        matr[row][col] = bool(bit)

    return matr


def deinterleave_right_first(n: int) -> tuple[int, int]:
    """Inverse of interleave_right_first — returns (row, col)."""
    row = col = 0
    for i in range(n.bit_length() // 2 + 1):
        row |= ((n >> (2 * i)) & 1) << i
        col |= ((n >> (2 * i + 1)) & 1) << i
    return row, col


def interleave_right_first(row: int, col: int) -> int:
    """Morton order with RIGHT-first preference (col-major bit interleaving)."""
    n = 0
    for i in range(max(row, col).bit_length()):
        n |= ((row >> i) & 1) << (2 * i)  # row bits in even positions
        n |= ((col >> i) & 1) << (2 * i + 1)  # col bits in odd positions
    return n


def bit_index_to_row_col(i: int) -> tuple[int, int]:
    """Given bit index i, return its (row, col) position in the top-heavy layout"""
    remaining = i
    width = 2
    base_row = 0

    while True:
        block_size = width * 2  # width * height
        if remaining < block_size:
            # In this block
            row_in_block = remaining // width
            col_in_block = remaining % width
            return (base_row + row_in_block, col_in_block)
        else:
            remaining -= block_size
            base_row += 2
            width *= 2


def row_col_to_bit_index(row: int, col: int) -> int:
    width = 2
    base_row = 0
    index = 0

    while True:
        if base_row <= row < base_row + 2 and col < width:
            return index + (row - base_row) * width + col
        else:
            index += width * 2
            base_row += 2
            width *= 2


def get_bits(n: int) -> List[int]:
    return [int(bit) for bit in bin(n)[2:]]


def validate_one_hot_matrix(matr: List[List[bool]]):
    for i, row in enumerate(matr):
        has_one = False
        for j, col in enumerate(row):
            if col is not False and col is not True:
                raise ValueError(f"invalid value at ({j}, {i}")
            else:
                if col == True:
                    if has_one:
                        raise ValueError(f"more than one entry in row {i}: {row}")
                    else:
                        has_one = True


def matrix_to_graph_entries(matr: List[List[bool]]):
    for i, row in enumerate(matr):
        for j, col in enumerate(row):
            if col is True:
                left = DictThing.from_int(i)
                right = DictThing.from_int(j)
                yield (left, right)


class DictThing:

    def __init__(self, entries):
        self.items = entries

    def __eq__(self, other) -> bool:
        if self.to_int() == other.to_int():
            return True
        return False

    def __repr__(self) -> str:
        return_str = f"DictThing({self.to_int()})\n"
        for entry in self.items:
            return_str += f"  {entry[0].to_int()} -> {entry[1].to_int()}\n"
        return return_str

    @classmethod
    def from_int(cls, n: int):
        matr = int_to_matrix(n)
        # validate_matrix(matr)
        entries = list(matrix_to_graph_entries(matr))
        return cls(entries)

    @classmethod
    def from_matr(cls, matr: List[List[bool]]):
        # validate_matrix(matr)
        return cls(matrix_to_graph_entries(matr))

    def to_int(self) -> int:
        triangle = self.to_matr()
        bits = []
        for row in triangle:
            bits.extend(int(b) for b in row)
        return int("".join(map(str, bits)), 2) if bits else 0

    def to_matr(self) -> List[List[bool]]:
        triangle = []
        for entry in self.items:
            left = entry[0].to_int()
            right = entry[1].to_int()
            if left >= len(triangle):
                triangle.extend([[] for _ in range(left - len(triangle) + 1)])
            if right >= len(triangle[left]):
                triangle[left].extend([False] * (right - len(triangle[left]) + 1))
            triangle[left][right] = True
        return triangle


if __name__ == "__main__":
    for i in range(10):
        print(f"{i}: {DictThing.from_int(i)}")
