#!/usr/bin/env python3

import math
from matrix_hilbert import hilbert_d_to_xy, hilbert_xy_to_d

def test_hilbert_pattern():
    """Test the Hilbert curve pattern for a 4x4 grid (16 positions)"""
    print("Testing Hilbert curve for 4x4 grid (n=4)")
    print("=" * 50)
    
    # Test conversion from distance to (x,y) coordinates
    print("Distance to (x,y) conversion:")
    print("d\t(x,y)\tExpected Pattern")
    print("-" * 40)
    
    # For a 4x4 Hilbert curve, the standard pattern should be:
    # Bottom-left quadrant: (0,0) -> (0,1) -> (1,1) -> (1,0)
    # Top-left quadrant: (0,3) -> (0,2) -> (1,2) -> (1,3)  
    # Top-right quadrant: (2,3) -> (2,2) -> (3,2) -> (3,3)
    # Bottom-right quadrant: (3,0) -> (2,0) -> (2,1) -> (3,1)
    
    expected_pattern = [
        (0, 0), (0, 1), (1, 1), (1, 0),  # Bottom-left quadrant (rotated)
        (0, 2), (0, 3), (1, 3), (1, 2),  # Top-left quadrant  
        (2, 2), (2, 3), (3, 3), (3, 2),  # Top-right quadrant
        (3, 1), (2, 1), (2, 0), (3, 0)   # Bottom-right quadrant (rotated)
    ]
    
    actual_pattern = []
    for d in range(16):
        x, y = hilbert_d_to_xy(4, d)
        actual_pattern.append((x, y))
        expected = expected_pattern[d] if d < len(expected_pattern) else "?"
        match = "✓" if (x, y) == expected else "✗"
        print(f"{d}\t({x},{y})\t{expected} {match}")
    
    print("\nActual pattern sequence:")
    print(" -> ".join([f"({x},{y})" for x, y in actual_pattern]))
    
    print("\nExpected pattern sequence:")
    print(" -> ".join([f"({x},{y})" for x, y in expected_pattern]))
    
    # Test reverse conversion
    print("\n" + "=" * 50)
    print("Testing reverse conversion (x,y) to distance:")
    print("(x,y)\td\tExpected d")
    print("-" * 30)
    
    for i, (x, y) in enumerate(actual_pattern):
        d = hilbert_xy_to_d(4, x, y)
        match = "✓" if d == i else "✗"
        print(f"({x},{y})\t{d}\t{i} {match}")
    
    # Visualize the grid
    print("\n" + "=" * 50)
    print("Grid visualization with distances:")
    grid = [[-1 for _ in range(4)] for _ in range(4)]
    
    for d in range(16):
        x, y = hilbert_d_to_xy(4, d)
        grid[y][x] = d  # Note: y is row, x is column
    
    for row in reversed(grid):  # Print from top to bottom
        print(" ".join([f"{val:2d}" if val >= 0 else "  " for val in row]))
    
    print("\nPattern analysis:")
    print("Quadrant 1 (0-3): ", [actual_pattern[i] for i in range(4)])
    print("Quadrant 2 (4-7): ", [actual_pattern[i] for i in range(4, 8)])
    print("Quadrant 3 (8-11):", [actual_pattern[i] for i in range(8, 12)])
    print("Quadrant 4 (12-15):", [actual_pattern[i] for i in range(12, 16)])

def test_rotation_function():
    """Test the hilbert_rot function with different inputs"""
    print("\n" + "=" * 50)
    print("Testing hilbert_rot function:")
    print("n\tx\ty\trx\try\t->\tx'\ty'")
    print("-" * 45)
    
    from matrix_hilbert import hilbert_rot
    
    # Test cases for different quadrant rotations
    test_cases = [
        (2, 0, 0, 0, 0),  # Bottom-left, no rotation
        (2, 1, 0, 1, 0),  # Bottom-right, flip diagonally  
        (2, 0, 1, 0, 1),  # Top-left, no rotation
        (2, 1, 1, 1, 1),  # Top-right, no rotation
    ]
    
    for n, x, y, rx, ry in test_cases:
        x_new, y_new = hilbert_rot(n, x, y, rx, ry)
        print(f"{n}\t{x}\t{y}\t{rx}\t{ry}\t->\t{x_new}\t{y_new}")

if __name__ == "__main__":
    test_hilbert_pattern()
    test_rotation_function()