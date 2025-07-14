#!/usr/bin/env python3

def correct_hilbert_d_to_xy(n, d):
    """
    Corrected Hilbert curve implementation based on standard algorithm
    The issue is in the bit extraction order in hilbert_d_to_xy
    """
    x = y = 0
    s = 1
    while s < n:
        # Extract bits correctly - this was the issue
        rx = int((d // 2) & 1)
        ry = int((d ^ rx) & 1)
        x, y = correct_hilbert_rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        d //= 4
        s *= 2
    return x, y

def correct_hilbert_rot(n, x, y, rx, ry):
    """
    Correct rotation function for Hilbert curve
    """
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        # Transpose
        x, y = y, x
    return x, y

def correct_hilbert_xy_to_d(n, x, y):
    """
    Corrected xy to d conversion
    """
    d = 0
    s = n // 2
    while s > 0:
        rx = int((x & s) > 0)
        ry = int((y & s) > 0)
        d += s * s * ((3 * rx) ^ ry)
        x, y = correct_hilbert_rot(s, x, y, rx, ry)
        s //= 2
    return d

def test_corrected_implementation():
    """Test the corrected implementation"""
    print("Testing Corrected Hilbert Implementation")
    print("=" * 50)
    
    print("2x2 grid:")
    for d in range(4):
        x, y = correct_hilbert_d_to_xy(2, d)
        print(f"{d}: ({x},{y})")
    
    print("\n4x4 grid:")
    points = []
    for d in range(16):
        x, y = correct_hilbert_d_to_xy(4, d)
        points.append((x, y))
        print(f"{d:2d}: ({x},{y})")
    
    # Visualize grid
    print("\nGrid visualization:")
    grid = [[-1 for _ in range(4)] for _ in range(4)]
    for d in range(16):
        x, y = correct_hilbert_d_to_xy(4, d)
        grid[y][x] = d
    
    for row in reversed(grid):
        print(" ".join([f"{val:2d}" for val in row]))
    
    # Test continuity
    print("\nTesting continuity:")
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        distance = abs(x2 - x1) + abs(y2 - y1)
        if distance != 1:
            print(f"Discontinuity between {i} and {i+1}: {(x1,y1)} -> {(x2,y2)}")
    
    # Compare with current implementation
    print("\nComparison with current implementation:")
    from matrix_hilbert import hilbert_d_to_xy
    
    differences = []
    for d in range(16):
        correct_xy = correct_hilbert_d_to_xy(4, d)
        current_xy = hilbert_d_to_xy(4, d)
        if correct_xy != current_xy:
            differences.append((d, correct_xy, current_xy))
    
    if differences:
        print("Differences found:")
        for d, correct, current in differences:
            print(f"d={d}: correct={correct}, current={current}")
    else:
        print("No differences - implementations are identical")

# Let's try a different approach - implement the textbook algorithm step by step
def textbook_hilbert_d_to_xy(n, d):
    """
    Textbook implementation of Hilbert curve
    Based on the recursive definition
    """
    if n == 1:
        return (0, 0)
    
    # This is a simplified recursive approach
    # For proper implementation, we need to handle the recursive structure
    return correct_hilbert_d_to_xy(n, d)

def manual_4x4_hilbert():
    """
    Manually construct the correct 4x4 Hilbert curve pattern
    Based on the recursive definition where each quadrant is a properly oriented 2x2 Hilbert
    """
    print("Manual 4x4 Hilbert Construction")
    print("=" * 40)
    
    # The correct 4x4 Hilbert should have these patterns:
    # Bottom-left: rotated 2x2 to connect from bottom
    # Top-left: normal 2x2 
    # Top-right: normal 2x2
    # Bottom-right: rotated 2x2 to connect from top
    
    # Base 2x2 pattern: (0,0) -> (0,1) -> (1,1) -> (1,0)
    base_pattern = [(0,0), (0,1), (1,1), (1,0)]
    
    print("Base 2x2 pattern:", " -> ".join([f"({x},{y})" for x, y in base_pattern]))
    
    # For 4x4, we need 4 quadrants with proper rotations
    # Bottom-left quadrant (positions 0-3): needs rotation to start at (0,0) and end at (0,1)
    # This should be: (0,0) -> (1,0) -> (1,1) -> (0,1) [90° clockwise rotation + reflection]
    
    # Top-left quadrant (positions 4-7): should connect from (0,1) to (1,2)
    # This should be: (0,2) -> (0,3) -> (1,3) -> (1,2) [translated up by 2]
    
    # Top-right quadrant (positions 8-11): should connect from (1,2) to (3,2)
    # This should be: (2,2) -> (2,3) -> (3,3) -> (3,2) [translated right by 2]
    
    # Bottom-right quadrant (positions 12-15): should connect from (3,2) to (3,0)
    # This should be: (3,1) -> (2,1) -> (2,0) -> (3,0) [rotated and translated]
    
    manual_pattern = [
        # Bottom-left (rotated)
        (0,0), (1,0), (1,1), (0,1),
        # Top-left 
        (0,2), (0,3), (1,3), (1,2),
        # Top-right
        (2,2), (2,3), (3,3), (3,2),
        # Bottom-right (rotated)
        (3,1), (2,1), (2,0), (3,0)
    ]
    
    print("\nManual 4x4 pattern:")
    for i, (x, y) in enumerate(manual_pattern):
        print(f"{i:2d}: ({x},{y})")
    
    # Check connectivity
    print("\nConnectivity check:")
    for i in range(len(manual_pattern) - 1):
        x1, y1 = manual_pattern[i]
        x2, y2 = manual_pattern[i + 1]
        distance = abs(x2 - x1) + abs(y2 - y1)
        if distance != 1:
            print(f"ERROR: Gap between {i} and {i+1}")
        else:
            print(f"{i:2d} -> {i+1:2d}: ({x1},{y1}) -> ({x2},{y2}) ✓")

if __name__ == "__main__":
    test_corrected_implementation()
    print("\n" + "=" * 60)
    manual_4x4_hilbert()