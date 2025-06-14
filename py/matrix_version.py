from typing import List
import math




def int_to_matrix(n: int) -> List[List[bool]]:
    order = math.log2(math.log2(n))
    order_ciel = math.ceil(order)
    matr_len = 2**(2**order_ciel)
    matr_dim = math.sqrt(matr_len)
    matr = []
    for i, bit in enumerate(get_bits(n)):
        if i % matr_dim > 0: 
            v_ix = i // matr_dim
            matr[v_ix] = bit
        else: 
            matr.append([bool(bit)])
    return matr

def get_bits(n: int) -> List[int]:
    [int(bit) for bit in bin(n)[2:]]


def validate_matrix(matr: List[List[bool]]):
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
    pass




class DictThing():


    def __init__(self, entries):
        self.items = entries


    def __eq__(): 
        pass

    @classmethod
    def from_int(n: int):
        matr = int_to_matrix(n)
        validate_matrix(matr)


    @classmethod
    def from_matr(matr: List[List[bool]]):
        validate_matrix(matr)
        return DictThing(matrix_to_graph_entries(matr))


    def to_int():
        pass

    def to_matr(): 
        pass

        

                
            



if __name__ == "main":
    print("test")


test.py
Displaying test.py.