#!/usr/bin/env python3

from matrix_hilbert import hilbert_d_to_xy

def analyze_hilbert_connectivity():
    """Analyze the connectivity and pattern of the current Hilbert curve"""
    print("Analyzing Hilbert Curve Connectivity")
    print("=" * 50)
    
    # Get the sequence of points
    points = []
    for d in range(16):
        x, y = hilbert_d_to_xy(4, d)
        points.append((x, y))
    
    print("Complete sequence:")
    for i, (x, y) in enumerate(points):
        print(f"{i:2d}: ({x},{y})")
    
    print("\nConnectivity analysis:")
    print("d\tFrom\t\tTo\t\tDirection")
    print("-" * 45)
    
    directions = {
        (1, 0): "Right",
        (-1, 0): "Left", 
        (0, 1): "Up",
        (0, -1): "Down"
    }
    
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        dx, dy = x2 - x1, y2 - y1
        direction = directions.get((dx, dy), f"({dx},{dy})")
        print(f"{i:2d}\t({x1},{y1})\t\t({x2},{y2})\t\t{direction}")
    
    # Check if all moves are unit distance
    print("\nDistance validation:")
    all_valid = True
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        distance = abs(x2 - x1) + abs(y2 - y1)  # Manhattan distance
        if distance != 1:
            print(f"Invalid move from {i} to {i+1}: distance = {distance}")
            all_valid = False
    
    if all_valid:
        print("✓ All moves are valid unit distances")
    
    # Analyze quadrant patterns
    print("\nQuadrant pattern analysis:")
    quadrants = [
        points[0:4],   # Quadrant 1 (bottom-left)
        points[4:8],   # Quadrant 2 (top-left) 
        points[8:12],  # Quadrant 3 (top-right)
        points[12:16]  # Quadrant 4 (bottom-right)
    ]
    
    for i, quad in enumerate(quadrants):
        print(f"\nQuadrant {i+1}: {quad}")
        # Describe the pattern
        moves = []
        for j in range(len(quad) - 1):
            x1, y1 = quad[j]
            x2, y2 = quad[j + 1]
            dx, dy = x2 - x1, y2 - y1
            moves.append(directions.get((dx, dy), f"({dx},{dy})"))
        print(f"Movement pattern: {' -> '.join(moves)}")
        
        # Check if it forms a connected curve within the 2x2 sub-quadrant
        min_x = min(p[0] for p in quad)
        max_x = max(p[0] for p in quad)
        min_y = min(p[1] for p in quad)
        max_y = max(p[1] for p in quad)
        print(f"Bounding box: x=[{min_x},{max_x}], y=[{min_y},{max_y}]")
        
        # Determine the shape
        if moves == ['Right', 'Up', 'Left']:
            print("Shape: Backwards C (expected for rotated quadrants)")
        elif moves == ['Up', 'Right', 'Down']:
            print("Shape: Forward C")
        elif moves == ['Right', 'Down', 'Left']:
            print("Shape: U shape")
        elif moves == ['Down', 'Right', 'Up']:
            print("Shape: Inverted U")
        else:
            print(f"Shape: Custom pattern")

def visualize_hilbert_step_by_step():
    """Show how the Hilbert curve is built step by step"""
    print("\n" + "=" * 50)
    print("Step-by-step Hilbert curve construction")
    print("=" * 50)
    
    # Show 2x2 case first
    print("2x2 Hilbert curve (n=2):")
    grid_2x2 = [[-1 for _ in range(2)] for _ in range(2)]
    for d in range(4):
        x, y = hilbert_d_to_xy(2, d)
        grid_2x2[y][x] = d
    
    for row in reversed(grid_2x2):
        print(" ".join([f"{val}" for val in row]))
    
    print("\nPattern: ", end="")
    for d in range(4):
        x, y = hilbert_d_to_xy(2, d)
        print(f"({x},{y})", end=" -> " if d < 3 else "\n")
    
    # Show how 4x4 is constructed from 2x2
    print("\n4x4 Hilbert curve construction:")
    print("The 4x4 curve should be made of four 2x2 sub-curves with appropriate rotations")
    
    # Analyze each 2x2 sub-quadrant in the 4x4 grid
    sub_quadrants = {
        "Bottom-left": [(0,0), (1,0), (0,1), (1,1)],
        "Top-left": [(0,2), (1,2), (0,3), (1,3)],
        "Top-right": [(2,2), (3,2), (2,3), (3,3)],
        "Bottom-right": [(2,0), (3,0), (2,1), (3,1)]
    }
    
    for name, coords in sub_quadrants.items():
        print(f"\n{name} sub-quadrant:")
        # Find which distances correspond to these coordinates
        distances = []
        for x, y in coords:
            for d in range(16):
                if hilbert_d_to_xy(4, d) == (x, y):
                    distances.append(d)
                    break
        
        distances.sort()
        pattern = [hilbert_d_to_xy(4, d) for d in distances]
        print(f"Distances: {distances}")
        print(f"Pattern: {' -> '.join([f'({x},{y})' for x, y in pattern])}")

if __name__ == "__main__":
    analyze_hilbert_connectivity()
    visualize_hilbert_step_by_step()