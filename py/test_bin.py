def from_int(x):
    return bin(x)[2:]


def to_int(s):
    return int(s, 2)


if __name__ == "__main__":
    print(bin(42))
