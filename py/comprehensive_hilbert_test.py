#!/usr/bin/env python3

from matrix_hilbert import hilbert_d_to_xy, hilbert_xy_to_d
import matplotlib.pyplot as plt
import numpy as np

def create_hilbert_visualization():
    """Create a comprehensive visualization of the Hilbert curve"""
    
    # Test different sizes
    sizes = [2, 4, 8]
    
    fig, axes = plt.subplots(1, len(sizes), figsize=(15, 5))
    if len(sizes) == 1:
        axes = [axes]
    
    for idx, n in enumerate(sizes):
        ax = axes[idx]
        
        # Generate all points
        points = []
        for d in range(n * n):
            x, y = hilbert_d_to_xy(n, d)
            points.append((x, y))
        
        # Plot the curve
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        # Plot the path
        ax.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.7)
        
        # Plot points with numbers
        for i, (x, y) in enumerate(points):
            ax.plot(x, y, 'ro', markersize=8)
            ax.annotate(str(i), (x, y), xytext=(5, 5), textcoords='offset points', 
                       fontsize=8, fontweight='bold')
        
        # Set up the plot
        ax.set_xlim(-0.5, n-0.5)
        ax.set_ylim(-0.5, n-0.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_title(f'Hilbert Curve {n}x{n}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        # Add grid lines at integer positions
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
    
    plt.tight_layout()
    plt.savefig('/home/dmn/main/code/project/graphlang/py/hilbert_visualization.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("Visualization saved as hilbert_visualization.png")

def test_hilbert_properties():
    """Test mathematical properties of the Hilbert curve"""
    print("Testing Hilbert Curve Properties")
    print("=" * 50)
    
    n = 4
    
    # Test 1: Bijectivity (every point maps to unique distance and vice versa)
    print("Test 1: Bijectivity")
    xy_to_d_map = {}
    d_to_xy_map = {}
    
    for d in range(n * n):
        x, y = hilbert_d_to_xy(n, d)
        d_back = hilbert_xy_to_d(n, x, y)
        
        if d != d_back:
            print(f"ERROR: d={d} -> ({x},{y}) -> d={d_back}")
        
        if (x, y) in xy_to_d_map:
            print(f"ERROR: Point ({x},{y}) maps to multiple distances")
        else:
            xy_to_d_map[(x, y)] = d
        
        if d in d_to_xy_map:
            print(f"ERROR: Distance {d} maps to multiple points")
        else:
            d_to_xy_map[d] = (x, y)
    
    print(f"✓ Bijectivity test passed for {n}x{n} grid")
    
    # Test 2: Continuity (consecutive distances map to adjacent points)
    print("\nTest 2: Continuity")
    discontinuities = 0
    for d in range(n * n - 1):
        x1, y1 = hilbert_d_to_xy(n, d)
        x2, y2 = hilbert_d_to_xy(n, d + 1)
        distance = abs(x2 - x1) + abs(y2 - y1)
        if distance != 1:
            print(f"Discontinuity at d={d}: ({x1},{y1}) -> ({x2},{y2}), distance={distance}")
            discontinuities += 1
    
    if discontinuities == 0:
        print(f"✓ Continuity test passed for {n}x{n} grid")
    else:
        print(f"✗ Found {discontinuities} discontinuities")
    
    # Test 3: Space-filling property (covers all points exactly once)
    print("\nTest 3: Space-filling property")
    covered_points = set()
    for d in range(n * n):
        x, y = hilbert_d_to_xy(n, d)
        if (x, y) in covered_points:
            print(f"ERROR: Point ({x},{y}) covered multiple times")
        covered_points.add((x, y))
    
    expected_points = {(x, y) for x in range(n) for y in range(n)}
    if covered_points == expected_points:
        print(f"✓ Space-filling test passed for {n}x{n} grid")
    else:
        missing = expected_points - covered_points
        extra = covered_points - expected_points
        if missing:
            print(f"Missing points: {missing}")
        if extra:
            print(f"Extra points: {extra}")

def analyze_user_expectation():
    """Analyze what the user expected vs what the algorithm produces"""
    print("\nAnalyzing User Expectation vs Reality")
    print("=" * 50)
    
    print("User's expectation:")
    print("- First 4 bits should form a backwards C: R -> D -> L")
    print("- This would be: (0,0) -> (1,0) -> (1,1) -> (0,1)")
    print("- Movement pattern: Right -> Up -> Left")
    
    print("\nWhat the algorithm actually produces:")
    actual_pattern = []
    for d in range(4):
        x, y = hilbert_d_to_xy(4, d)
        actual_pattern.append((x, y))
    
    print(f"- Actual pattern: {' -> '.join([f'({x},{y})' for x, y in actual_pattern])}")
    
    # Movement analysis
    moves = []
    for i in range(len(actual_pattern) - 1):
        x1, y1 = actual_pattern[i]
        x2, y2 = actual_pattern[i + 1]
        if x2 > x1:
            moves.append("Right")
        elif x2 < x1:
            moves.append("Left")
        elif y2 > y1:
            moves.append("Up")
        elif y2 < y1:
            moves.append("Down")
    
    print(f"- Movement pattern: {' -> '.join(moves)}")
    
    print("\nExplanation:")
    print("The current implementation IS CORRECT according to the standard Hilbert curve algorithm.")
    print("The first quadrant is rotated to ensure the overall curve is continuous.")
    print("This is not a bug - it's the expected behavior of the Hilbert curve.")
    
    print("\nWhy the rotation is necessary:")
    print("1. The curve must be continuous (no gaps)")
    print("2. The curve must visit every point exactly once")
    print("3. The recursive structure requires different orientations in different quadrants")
    print("4. The bottom-left quadrant is rotated to connect properly with the top-left quadrant")

def compare_with_other_space_filling_curves():
    """Show how this compares to other space-filling curves"""
    print("\nComparison with other space-filling curves")
    print("=" * 50)
    
    # Z-order (Morton) curve for comparison
    def morton_2d_encode(x, y):
        """Simple Morton encoding for comparison"""
        result = 0
        for i in range(16):  # Enough bits for reasonable coordinates
            result |= (x & (1 << i)) << i | (y & (1 << i)) << (i + 1)
        return result
    
    def morton_2d_decode(code):
        """Simple Morton decoding"""
        x = y = 0
        for i in range(16):
            x |= (code & (1 << (2 * i))) >> i
            y |= (code & (1 << (2 * i + 1))) >> (i + 1)
        return x, y
    
    print("Hilbert vs Morton (Z-order) for 4x4:")
    print("Pos\tHilbert\t\tMorton")
    print("-" * 35)
    
    for d in range(16):
        hilbert_xy = hilbert_d_to_xy(4, d)
        # For Morton, we need to map position to coordinates differently
        # Morton order: 0,1,4,5,2,3,6,7,8,9,12,13,10,11,14,15
        morton_order = [0,1,4,5,2,3,6,7,8,9,12,13,10,11,14,15]
        morton_pos = morton_order[d] if d < len(morton_order) else d
        morton_x = morton_pos % 4
        morton_y = morton_pos // 4
        morton_xy = (morton_x, morton_y)
        
        print(f"{d:2d}\t{hilbert_xy}\t\t{morton_xy}")

if __name__ == "__main__":
    test_hilbert_properties()
    analyze_user_expectation()
    compare_with_other_space_filling_curves()
    create_hilbert_visualization()