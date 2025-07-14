#!/usr/bin/env python3

def reference_hilbert_d_to_xy(n, d):
    """Reference implementation of Hilbert curve d->xy conversion"""
    x = y = 0
    s = 1
    while s < n:
        rx = (d // 2) & 1
        ry = (d ^ rx) & 1
        x, y = reference_hilbert_rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        d //= 4
        s *= 2
    return x, y

def reference_hilbert_rot(n, x, y, rx, ry):
    """Reference rotation function for Hilbert curve"""
    if ry == 0:
        if rx == 1:
            # Rotate 180 degrees
            x = n - 1 - x
            y = n - 1 - y
        # Swap x and y (rotate 90 degrees)
        x, y = y, x
    return x, y

def reference_hilbert_xy_to_d(n, x, y):
    """Reference implementation of Hilbert curve xy->d conversion"""
    d = 0
    s = n // 2
    while s > 0:
        rx = (x & s) > 0
        ry = (y & s) > 0
        d += s * s * ((3 * rx) ^ ry)
        x, y = reference_hilbert_rot(s, x, y, rx, ry)
        s //= 2
    return d

def test_reference_vs_current():
    """Compare reference implementation with current implementation"""
    print("Comparing Reference vs Current Implementation:")
    print("=" * 60)
    print("d\tRef (x,y)\tCur (x,y)\tMatch")
    print("-" * 50)
    
    from matrix_hilbert import hilbert_d_to_xy
    
    for d in range(16):
        ref_x, ref_y = reference_hilbert_d_to_xy(4, d)
        cur_x, cur_y = hilbert_d_to_xy(4, d)
        match = "✓" if (ref_x, ref_y) == (cur_x, cur_y) else "✗"
        print(f"{d}\t({ref_x},{ref_y})\t\t({cur_x},{cur_y})\t\t{match}")
    
    print("\nReference Grid:")
    ref_grid = [[-1 for _ in range(4)] for _ in range(4)]
    for d in range(16):
        x, y = reference_hilbert_d_to_xy(4, d)
        ref_grid[y][x] = d
    
    for row in reversed(ref_grid):
        print(" ".join([f"{val:2d}" if val >= 0 else "  " for val in row]))
    
    print("\nCurrent Grid:")
    cur_grid = [[-1 for _ in range(4)] for _ in range(4)]
    for d in range(16):
        x, y = hilbert_d_to_xy(4, d)
        cur_grid[y][x] = d
    
    for row in reversed(cur_grid):
        print(" ".join([f"{val:2d}" if val >= 0 else "  " for val in row]))
    
    # Test the rotation functions specifically
    print("\nTesting rotation functions:")
    print("Input\t\tRef rot\t\tCur rot\t\tMatch")
    print("-" * 60)
    
    from matrix_hilbert import hilbert_rot
    
    test_cases = [
        (2, 0, 0, 0, 0),
        (2, 1, 0, 0, 0), 
        (2, 0, 1, 0, 0),
        (2, 1, 1, 0, 0),
        (2, 0, 0, 1, 0),
        (2, 1, 0, 1, 0),
        (2, 0, 1, 1, 0),
        (2, 1, 1, 1, 0),
        (2, 0, 0, 0, 1),
        (2, 1, 0, 0, 1),
        (2, 0, 1, 0, 1),
        (2, 1, 1, 0, 1),
        (2, 0, 0, 1, 1),
        (2, 1, 0, 1, 1),
        (2, 0, 1, 1, 1),
        (2, 1, 1, 1, 1),
    ]
    
    for n, x, y, rx, ry in test_cases:
        ref_x, ref_y = reference_hilbert_rot(n, x, y, rx, ry)
        cur_x, cur_y = hilbert_rot(n, x, y, rx, ry)
        match = "✓" if (ref_x, ref_y) == (cur_x, cur_y) else "✗"
        print(f"({n},{x},{y},{rx},{ry})\t({ref_x},{ref_y})\t\t({cur_x},{cur_y})\t\t{match}")

if __name__ == "__main__":
    test_reference_vs_current()