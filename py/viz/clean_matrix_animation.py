from manim import *
import numpy as np
from test_eval import create_matrix_graph, set_matrix_curve_type
from trajectory_animation import calculate_trajectory
from matrix_trajectory_animation import get_matrix_entries_as_coordinates
from typing import List, Tuple


def create_clean_matrix(coordinates: List[Tuple[int, int]], max_size: int = 8) -> VGroup:
    """
    Create a very clean matrix visualization with no text at all.
    """
    if not coordinates:
        # Return empty 2x2 matrix
        matrix_group = VGroup()
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=0.3, color=WHITE, fill_opacity=0.05, stroke_color=GRAY, stroke_width=1)
                cell.shift(RIGHT * j * 0.32 + DOWN * i * 0.32)
                matrix_group.add(cell)
        return matrix_group
    
    # Determine matrix size
    max_coord = max(max(coord) for coord in coordinates) if coordinates else 0
    matrix_size = min(max_size, max(2, 2 ** (max_coord.bit_length())))
    
    matrix_group = VGroup()
    
    # Smaller cells for larger matrices
    cell_size = max(0.15, 0.6 / matrix_size)  # Scale down for larger matrices
    spacing = cell_size + 0.02
    
    # Create clean grid
    for i in range(matrix_size):
        for j in range(matrix_size):
            if (i, j) in coordinates:
                # Filled cell - bright blue
                cell = Square(side_length=cell_size, color=BLUE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
            else:
                # Empty cell - very light gray
                cell = Square(side_length=cell_size, color=WHITE, fill_opacity=0.05, stroke_color=GRAY, stroke_width=0.5)
            
            cell.shift(RIGHT * j * spacing + DOWN * i * spacing)
            matrix_group.add(cell)
    
    return matrix_group


class CleanMatrixTrajectory(Scene):
    """Clean matrix trajectory visualization with no text, just matrices."""
    
    def construct(self):
        # Set curve type
        set_matrix_curve_type("morton")
        
        # Calculate trajectory with a much larger number
        start_node = create_matrix_graph(127)  # Much larger number
        trajectory = calculate_trajectory(start_node, max_steps=5)
        
        # Show clean matrix evolution
        current_matrix = None
        for i, node in enumerate(trajectory):
            coordinates = get_matrix_entries_as_coordinates(node)
            matrix_visual = create_clean_matrix(coordinates, max_size=8)  # Larger matrix
            matrix_visual.move_to(ORIGIN)
            
            if i == 0:
                # First matrix
                self.play(Create(matrix_visual), run_time=1.5)
                current_matrix = matrix_visual
            else:
                # Transform to next matrix
                self.play(Transform(current_matrix, matrix_visual), run_time=1.5)
            
            self.wait(1.2)


class CleanDualTrajectory(Scene):
    """Side-by-side comparison with no text, just matrices."""
    
    def construct(self):
        # Calculate both trajectories with a larger number
        start_val = 255  # Much larger number
        
        # Morton trajectory
        set_matrix_curve_type("morton")
        morton_start = create_matrix_graph(start_val)
        morton_trajectory = calculate_trajectory(morton_start, max_steps=4)
        
        # Hilbert trajectory  
        set_matrix_curve_type("hilbert")
        hilbert_start = create_matrix_graph(start_val)
        hilbert_trajectory = calculate_trajectory(hilbert_start, max_steps=4)
        
        # Animate side by side
        max_steps = max(len(morton_trajectory), len(hilbert_trajectory))
        morton_current = None
        hilbert_current = None
        
        for step in range(max_steps):
            animations = []
            
            # Morton (left)
            if step < len(morton_trajectory):
                morton_coords = get_matrix_entries_as_coordinates(morton_trajectory[step])
                morton_matrix = create_clean_matrix(morton_coords, max_size=8)  # Larger matrix
                morton_matrix.shift(LEFT * 4.5)  # More space for larger matrices
                
                if step == 0:
                    animations.append(Create(morton_matrix))
                    morton_current = morton_matrix
                else:
                    animations.append(Transform(morton_current, morton_matrix))
            
            # Hilbert (right)
            if step < len(hilbert_trajectory):
                hilbert_coords = get_matrix_entries_as_coordinates(hilbert_trajectory[step])
                hilbert_matrix = create_clean_matrix(hilbert_coords, max_size=8)  # Larger matrix
                hilbert_matrix.shift(RIGHT * 4.5)  # More space for larger matrices
                
                if step == 0:
                    animations.append(Create(hilbert_matrix))
                    hilbert_current = hilbert_matrix
                else:
                    animations.append(Transform(hilbert_current, hilbert_matrix))
            
            if animations:
                self.play(*animations, run_time=1.5)
            
            self.wait(1.0)


class MinimalMatrixFlow(Scene):
    """Minimal animation showing just the flow of matrices."""
    
    def construct(self):
        # Multiple larger starting points, show their trajectories in sequence
        starting_points = [63, 127, 255, 511]  # Much larger numbers
        
        set_matrix_curve_type("morton")
        
        for start_val in starting_points:
            start_node = create_matrix_graph(start_val)
            trajectory = calculate_trajectory(start_node, max_steps=3)
            
            # Show trajectory for this starting point
            current_matrix = None
            for i, node in enumerate(trajectory):
                coordinates = get_matrix_entries_as_coordinates(node)
                matrix_visual = create_clean_matrix(coordinates, max_size=8)  # Larger matrix
                matrix_visual.move_to(ORIGIN)
                
                if i == 0:
                    self.play(Create(matrix_visual), run_time=1.0)
                    current_matrix = matrix_visual
                else:
                    self.play(Transform(current_matrix, matrix_visual), run_time=1.0)
                
                self.wait(0.8)
            
            # Brief pause between trajectories
            self.wait(0.5)
            
            # Clear for next trajectory (except on last one)
            if start_val != starting_points[-1]:
                self.play(FadeOut(current_matrix), run_time=0.5)


if __name__ == "__main__":
    # To render: manim -pql clean_matrix_animation.py CleanMatrixTrajectory
    # To render: manim -pql clean_matrix_animation.py CleanDualTrajectory  
    # To render: manim -pql clean_matrix_animation.py MinimalMatrixFlow
    pass