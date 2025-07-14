from test_eval import create_matrix_graph, set_matrix_curve_type
from matrix_trajectory_animation import get_matrix_entries_as_coordinates


def test_curve_ordering():
    """Simple test to see if Morton and Hilbert produce different orderings."""
    
    print("=== Simple Curve Ordering Test ===\n")
    
    # Test a range of values
    for val in [5, 7, 9, 11, 13, 17, 19, 21, 23]:
        print(f"Testing value: {val}")
        
        # Morton
        set_matrix_curve_type("morton")
        morton_node = create_matrix_graph(val)
        morton_coords = sorted(get_matrix_entries_as_coordinates(morton_node))
        
        # Hilbert
        set_matrix_curve_type("hilbert")
        hilbert_node = create_matrix_graph(val)
        hilbert_coords = sorted(get_matrix_entries_as_coordinates(hilbert_node))
        
        print(f"  Morton:  {morton_coords}")
        print(f"  Hilbert: {hilbert_coords}")
        
        if morton_coords == hilbert_coords:
            print(f"  ❌ IDENTICAL")
        else:
            print(f"  ✅ DIFFERENT")
            # Show the differences
            morton_set = set(morton_coords)
            hilbert_set = set(hilbert_coords)
            only_morton = morton_set - hilbert_set
            only_hilbert = hilbert_set - morton_set
            if only_morton:
                print(f"     Only in Morton: {sorted(only_morton)}")
            if only_hilbert:
                print(f"     Only in Hilbert: {sorted(only_hilbert)}")
        
        print()


def visualize_difference():
    """Show a clear visual of the difference for a specific value."""
    
    val = 21  # This should show a difference
    
    print(f"=== Visual Comparison for {val} ===\n")
    
    # Morton
    set_matrix_curve_type("morton")
    morton_node = create_matrix_graph(val)
    morton_matrix = morton_node.to_matrix()
    
    # Hilbert
    set_matrix_curve_type("hilbert")  
    hilbert_node = create_matrix_graph(val)
    hilbert_matrix = hilbert_node.to_matrix()
    
    print("Morton pattern:")
    print_matrix(morton_matrix)
    
    print("\nHilbert pattern:")
    print_matrix(hilbert_matrix)
    
    # Show differences
    print("\nDifferences (M=Morton only, H=Hilbert only, B=Both):")
    print_difference_matrix(morton_matrix, hilbert_matrix)


def print_matrix(matrix):
    """Print a boolean matrix with filled squares."""
    if not matrix:
        print("  (empty)")
        return
    
    for row in matrix:
        print("  " + "".join("█" if cell else "·" for cell in row))


def print_difference_matrix(matrix1, matrix2):
    """Print differences between two matrices."""
    if not matrix1 or not matrix2:
        print("  (empty matrices)")
        return
    
    max_dim = max(len(matrix1), len(matrix2))
    
    # Pad matrices to same size
    m1 = [[False] * max_dim for _ in range(max_dim)]
    m2 = [[False] * max_dim for _ in range(max_dim)]
    
    for i in range(min(len(matrix1), max_dim)):
        for j in range(min(len(matrix1[i]), max_dim)):
            m1[i][j] = matrix1[i][j]
    
    for i in range(min(len(matrix2), max_dim)):
        for j in range(min(len(matrix2[i]), max_dim)):
            m2[i][j] = matrix2[i][j]
    
    for i in range(max_dim):
        row_str = "  "
        for j in range(max_dim):
            if m1[i][j] and m2[i][j]:
                row_str += "B"  # Both
            elif m1[i][j]:
                row_str += "M"  # Morton only
            elif m2[i][j]:
                row_str += "H"  # Hilbert only
            else:
                row_str += "·"  # Neither
        print(row_str)


if __name__ == "__main__":
    test_curve_ordering()
    print("\n" + "="*50 + "\n")
    visualize_difference()