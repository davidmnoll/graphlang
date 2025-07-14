#!/usr/bin/env python3

from matrix_hilbert import hilbert_d_to_xy

def create_ascii_visualization():
    """Create ASCII visualization of the Hilbert curve"""
    print("ASCII Visualization of 4x4 Hilbert Curve")
    print("=" * 50)
    
    # Create the grid with positions
    grid = [['  ' for _ in range(4)] for _ in range(4)]
    
    for d in range(16):
        x, y = hilbert_d_to_xy(4, d)
        grid[3-y][x] = f"{d:2d}"  # Flip y to match standard coordinate system
    
    print("Grid with positions (top-left is high Y):")
    for row in grid:
        print(' '.join(row))
    
    # Show the path with arrows
    print("\nPath visualization:")
    path_grid = [['.' for _ in range(7)] for _ in range(7)]  # Expanded grid for arrows
    
    points = []
    for d in range(16):
        x, y = hilbert_d_to_xy(4, d)
        points.append((x, y))
        # Place number in expanded grid
        path_grid[6-(2*y)][2*x] = str(d % 10)
    
    # Add arrows between consecutive points
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        # Calculate arrow position and direction
        arrow_x = 2*x1 + (x2 - x1)
        arrow_y = 6-(2*y1) - (y2 - y1)
        
        if x2 > x1:
            arrow = '→'
        elif x2 < x1:
            arrow = '←'
        elif y2 > y1:
            arrow = '↑'
        elif y2 < y1:
            arrow = '↓'
        else:
            arrow = '•'
        
        if 0 <= arrow_x < 7 and 0 <= arrow_y < 7:
            path_grid[arrow_y][arrow_x] = arrow
    
    for row in path_grid:
        print(' '.join(row))
    
    # Analyze quadrant patterns
    print("\nQuadrant Analysis:")
    print("-" * 30)
    
    quadrants = [
        ("Bottom-Left", points[0:4]),
        ("Top-Left", points[4:8]),
        ("Top-Right", points[8:12]),
        ("Bottom-Right", points[12:16])
    ]
    
    for name, quad_points in quadrants:
        print(f"\n{name} quadrant:")
        print(f"Points: {' → '.join([f'({x},{y})' for x, y in quad_points])}")
        
        # Calculate movement directions
        moves = []
        for j in range(len(quad_points) - 1):
            x1, y1 = quad_points[j]
            x2, y2 = quad_points[j + 1]
            if x2 > x1:
                moves.append("Right")
            elif x2 < x1:
                moves.append("Left")
            elif y2 > y1:
                moves.append("Up")
            else:
                moves.append("Down")
        
        print(f"Moves: {' → '.join(moves)}")
        
        # Describe the shape
        if moves == ["Right", "Up", "Left"]:
            shape = "U-shape (rotated Hilbert base)"
        elif moves == ["Up", "Right", "Down"]:
            shape = "C-shape (normal Hilbert orientation)"
        elif moves == ["Up", "Right", "Down"]:
            shape = "Forward C"
        elif moves == ["Left", "Down", "Right"]:
            shape = "Inverted U (rotated)"
        else:
            shape = "Custom pattern"
        
        print(f"Shape: {shape}")

def show_recursive_structure():
    """Show how the 4x4 Hilbert is built from 2x2 components"""
    print("\n" + "=" * 60)
    print("Recursive Structure Analysis")
    print("=" * 60)
    
    print("Base 2x2 Hilbert curve:")
    base_2x2 = []
    for d in range(4):
        x, y = hilbert_d_to_xy(2, d)
        base_2x2.append((x, y))
    
    print(f"Pattern: {' → '.join([f'({x},{y})' for x, y in base_2x2])}")
    
    # Show 2x2 grid
    grid_2x2 = [['.' for _ in range(2)] for _ in range(2)]
    for d in range(4):
        x, y = hilbert_d_to_xy(2, d)
        grid_2x2[1-y][x] = str(d)
    
    print("2x2 grid:")
    for row in grid_2x2:
        print(' '.join(row))
    
    print("\nHow 4x4 is constructed:")
    print("The 4x4 Hilbert curve consists of four 2x2 subcurves with different orientations:")
    
    # Analyze each 2x2 section of the 4x4 curve
    sections = {
        "Bottom-left (0,0)-(1,1)": [(0,0), (1,0), (1,1), (0,1)],
        "Top-left (0,2)-(1,3)": [(0,2), (0,3), (1,3), (1,2)], 
        "Top-right (2,2)-(3,3)": [(2,2), (2,3), (3,3), (3,2)],
        "Bottom-right (2,0)-(3,1)": [(3,1), (2,1), (2,0), (3,0)]
    }
    
    for section_name, expected_coords in sections.items():
        print(f"\n{section_name}:")
        # Find which distances correspond to these coordinates
        actual_distances = []
        for d in range(16):
            x, y = hilbert_d_to_xy(4, d)
            if (x, y) in expected_coords:
                actual_distances.append(d)
        
        actual_distances.sort()
        actual_pattern = [hilbert_d_to_xy(4, d) for d in actual_distances]
        
        print(f"Distances: {actual_distances}")
        print(f"Pattern: {' → '.join([f'({x},{y})' for x, y in actual_pattern])}")
        
        # Compare with base 2x2 (normalized to start at 0,0)
        normalized_pattern = []
        min_x = min(x for x, y in actual_pattern)
        min_y = min(y for x, y in actual_pattern)
        for x, y in actual_pattern:
            normalized_pattern.append((x - min_x, y - min_y))
        
        print(f"Normalized: {' → '.join([f'({x},{y})' for x, y in normalized_pattern])}")
        
        if normalized_pattern == base_2x2:
            print("✓ Matches base 2x2 pattern")
        else:
            print("✗ Different from base 2x2 - this is expected due to rotations!")

if __name__ == "__main__":
    create_ascii_visualization()
    show_recursive_structure()