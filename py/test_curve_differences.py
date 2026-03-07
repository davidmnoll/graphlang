from test_eval import create_matrix_graph, set_matrix_curve_type
from matrix_trajectory_animation import get_matrix_entries_as_coordinates
import numpy as np


def test_curve_differences():
    """Test to verify Morton vs Hilbert are actually different algorithms."""
    
    print("=== Testing Morton vs Hilbert Curve Differences ===\n")
    
    # Test several values to see the patterns
    test_values = [7, 15, 31, 63, 127, 255]
    
    for val in test_values:
        print(f"Testing value: {val} (binary: {bin(val)})")
        
        # Get Morton representation
        set_matrix_curve_type("morton")
        morton_node = create_matrix_graph(val)
        morton_coords = get_matrix_entries_as_coordinates(morton_node)
        morton_matrix = morton_node.to_matrix()
        
        # Get Hilbert representation  
        set_matrix_curve_type("hilbert")
        hilbert_node = create_matrix_graph(val)
        hilbert_coords = get_matrix_entries_as_coordinates(hilbert_node)
        hilbert_matrix = hilbert_node.to_matrix()
        
        print(f"  Morton coordinates:  {sorted(morton_coords)}")
        print(f"  Hilbert coordinates: {sorted(hilbert_coords)}")
        
        # Check if they're the same
        if morton_coords == hilbert_coords:
            print(f"  ⚠️  IDENTICAL coordinates!")
        else:
            print(f"  ✓  Different coordinates")
        
        # Check if one is just a transformation of the other
        if set(morton_coords) == set(hilbert_coords):
            print(f"  ⚠️  Same set of coordinates (just reordered)")
        
        # Check matrix dimensions
        print(f"  Morton matrix size:  {len(morton_matrix)}x{len(morton_matrix[0]) if morton_matrix else 0}")
        print(f"  Hilbert matrix size: {len(hilbert_matrix)}x{len(hilbert_matrix[0]) if hilbert_matrix else 0}")
        
        print()


def visualize_matrices():
    """Visualize the actual matrices to see the patterns."""
    
    print("=== Visual Matrix Comparison ===\n")
    
    test_val = 127
    
    # Morton
    set_matrix_curve_type("morton")
    morton_node = create_matrix_graph(test_val)
    morton_matrix = morton_node.to_matrix()
    
    # Hilbert
    set_matrix_curve_type("hilbert")
    hilbert_node = create_matrix_graph(test_val)
    hilbert_matrix = hilbert_node.to_matrix()
    
    print(f"Value: {test_val}")
    print("\nMorton Matrix:")
    print_matrix(morton_matrix)
    
    print("\nHilbert Matrix:")
    print_matrix(hilbert_matrix)
    
    # Check if they're related by simple transformations
    print("\nTransformation checks:")
    
    # Check transpose
    if matrices_equal(morton_matrix, transpose_matrix(hilbert_matrix)):
        print("  Hilbert = Morton^T (transpose)")
    
    # Check horizontal flip
    if matrices_equal(morton_matrix, flip_horizontal(hilbert_matrix)):
        print("  Hilbert = Morton flipped horizontally")
    
    # Check vertical flip
    if matrices_equal(morton_matrix, flip_vertical(hilbert_matrix)):
        print("  Hilbert = Morton flipped vertically")
    
    # Check rotation
    if matrices_equal(morton_matrix, rotate_90(hilbert_matrix)):
        print("  Hilbert = Morton rotated 90°")
    
    if not any([
        matrices_equal(morton_matrix, transpose_matrix(hilbert_matrix)),
        matrices_equal(morton_matrix, flip_horizontal(hilbert_matrix)),
        matrices_equal(morton_matrix, flip_vertical(hilbert_matrix)),
        matrices_equal(morton_matrix, rotate_90(hilbert_matrix))
    ]):
        print("  ✓ Matrices are not simple transformations of each other")


def print_matrix(matrix):
    """Pretty print a boolean matrix."""
    if not matrix:
        print("  (empty)")
        return
    
    for row in matrix:
        print("  " + "".join("█" if cell else "·" for cell in row))


def transpose_matrix(matrix):
    """Transpose a matrix."""
    if not matrix:
        return matrix
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def flip_horizontal(matrix):
    """Flip matrix horizontally."""
    if not matrix:
        return matrix
    return [row[::-1] for row in matrix]


def flip_vertical(matrix):
    """Flip matrix vertically."""
    if not matrix:
        return matrix
    return matrix[::-1]


def rotate_90(matrix):
    """Rotate matrix 90 degrees clockwise."""
    if not matrix:
        return matrix
    n = len(matrix)
    return [[matrix[n-1-j][i] for j in range(n)] for i in range(n)]


def matrices_equal(m1, m2):
    """Check if two matrices are equal."""
    if len(m1) != len(m2):
        return False
    for i in range(len(m1)):
        if len(m1[i]) != len(m2[i]):
            return False
        for j in range(len(m1[i])):
            if m1[i][j] != m2[i][j]:
                return False
    return True


def test_underlying_algorithms():
    """Test the actual Morton vs Hilbert algorithms directly."""
    
    print("=== Testing Underlying Algorithms ===\n")
    
    # Import the matrix classes directly
    from matrix_morton import MatrixMorton
    from matrix_hilbert import MatrixHilbert
    
    test_val = 15
    
    print(f"Testing value: {test_val}")
    
    # Create instances directly
    morton = MatrixMorton.from_int(test_val)
    hilbert = MatrixHilbert.from_int(test_val)
    
    print(f"Morton to_int(): {morton.to_int()}")
    print(f"Hilbert to_int(): {hilbert.to_int()}")
    
    morton_matrix = morton.to_matrix()
    hilbert_matrix = hilbert.to_matrix()
    
    print("\nDirect algorithm results:")
    print("Morton:")
    print_matrix(morton_matrix)
    print("Hilbert:")
    print_matrix(hilbert_matrix)
    
    # Check entries
    print(f"\nMorton entries: {len(morton.entries)}")
    for i, entry in enumerate(morton.entries):
        print(f"  {i}: {entry[0].to_int()} -> {entry[1].to_int()}")
    
    print(f"\nHilbert entries: {len(hilbert.entries)}")
    for i, entry in enumerate(hilbert.entries):
        print(f"  {i}: {entry[0].to_int()} -> {entry[1].to_int()}")


if __name__ == "__main__":
    test_curve_differences()
    print("\n" + "="*50 + "\n")
    visualize_matrices()
    print("\n" + "="*50 + "\n")
    test_underlying_algorithms()