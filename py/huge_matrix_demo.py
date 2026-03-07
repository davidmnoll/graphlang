from manim import *
import numpy as np
from test_eval import create_matrix_graph, set_matrix_curve_type
from trajectory_animation import calculate_trajectory
from matrix_trajectory_animation import get_matrix_entries_as_coordinates
from typing import List, Tuple


def create_huge_matrix(coordinates: List[Tuple[int, int]], max_size: int = 16) -> VGroup:
    """
    Create matrix visualization for very large numbers.
    """
    if not coordinates:
        return VGroup()
    
    # Determine matrix size
    max_coord = max(max(coord) for coord in coordinates) if coordinates else 0
    matrix_size = min(max_size, max(2, 2 ** (max_coord.bit_length())))
    
    matrix_group = VGroup()
    
    # Very small cells for huge matrices
    cell_size = max(0.08, 0.8 / matrix_size)  # Scale down for larger matrices
    spacing = cell_size + 0.01
    
    # Create clean grid
    for i in range(matrix_size):
        for j in range(matrix_size):
            if (i, j) in coordinates:
                # Filled cell - bright blue
                cell = Square(side_length=cell_size, color=BLUE, fill_opacity=1.0, stroke_color=WHITE, stroke_width=0.5)
            else:
                # Empty cell - very light gray
                cell = Square(side_length=cell_size, color=WHITE, fill_opacity=0.02, stroke_color=GRAY, stroke_width=0.2)
            
            cell.shift(RIGHT * j * spacing + DOWN * i * spacing)
            matrix_group.add(cell)
    
    return matrix_group


class HugeMatrixTrajectory(Scene):
    """Matrix trajectory with very large starting numbers."""
    
    def construct(self):
        set_matrix_curve_type("morton")
        
        # Use a very large number to see complex patterns
        start_node = create_matrix_graph(1023)  # 2^10 - 1, should create complex pattern
        trajectory = calculate_trajectory(start_node, max_steps=4)
        
        # Show evolution
        current_matrix = None
        for i, node in enumerate(trajectory):
            coordinates = get_matrix_entries_as_coordinates(node)
            matrix_visual = create_huge_matrix(coordinates, max_size=16)
            matrix_visual.move_to(ORIGIN)
            
            if i == 0:
                self.play(Create(matrix_visual), run_time=2.0)
                current_matrix = matrix_visual
            else:
                self.play(Transform(current_matrix, matrix_visual), run_time=2.0)
            
            self.wait(1.5)


class MassiveMatrixComparison(Scene):
    """Compare huge matrices between Morton and Hilbert."""
    
    def construct(self):
        # Use a massive number
        start_val = 2047  # 2^11 - 1
        
        # Morton trajectory
        set_matrix_curve_type("morton")
        morton_start = create_matrix_graph(start_val)
        morton_trajectory = calculate_trajectory(morton_start, max_steps=3)
        
        # Hilbert trajectory  
        set_matrix_curve_type("hilbert")
        hilbert_start = create_matrix_graph(start_val)
        hilbert_trajectory = calculate_trajectory(hilbert_start, max_steps=3)
        
        # Show side by side
        max_steps = max(len(morton_trajectory), len(hilbert_trajectory))
        morton_current = None
        hilbert_current = None
        
        for step in range(max_steps):
            animations = []
            
            # Morton (left)
            if step < len(morton_trajectory):
                morton_coords = get_matrix_entries_as_coordinates(morton_trajectory[step])
                morton_matrix = create_huge_matrix(morton_coords, max_size=16)
                morton_matrix.shift(LEFT * 5)
                
                if step == 0:
                    animations.append(Create(morton_matrix))
                    morton_current = morton_matrix
                else:
                    animations.append(Transform(morton_current, morton_matrix))
            
            # Hilbert (right)
            if step < len(hilbert_trajectory):
                hilbert_coords = get_matrix_entries_as_coordinates(hilbert_trajectory[step])
                hilbert_matrix = create_huge_matrix(hilbert_coords, max_size=16)
                hilbert_matrix.shift(RIGHT * 5)
                
                if step == 0:
                    animations.append(Create(hilbert_matrix))
                    hilbert_current = hilbert_matrix
                else:
                    animations.append(Transform(hilbert_current, hilbert_matrix))
            
            if animations:
                self.play(*animations, run_time=2.0)
            
            self.wait(1.2)


if __name__ == "__main__":
    # To render: manim -pql huge_matrix_demo.py HugeMatrixTrajectory
    # To render: manim -pql huge_matrix_demo.py MassiveMatrixComparison
    pass