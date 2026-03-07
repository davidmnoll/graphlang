from manim import *
import numpy as np
from test_eval import create_matrix_graph, set_matrix_curve_type
from trajectory_animation import calculate_trajectory
from typing import List, Tuple, Dict


def get_matrix_entries_as_coordinates(node) -> List[Tuple[int, int]]:
    """
    Extract the matrix entries as (row, col) coordinate pairs.
    
    Args:
        node: The graph node to extract coordinates from
        
    Returns:
        List of (row, col) tuples representing filled matrix positions
    """
    coordinates = []
    try:
        for entry in node.entries:
            src_val = entry[0].to_int()
            dst_val = entry[1].to_int()
            coordinates.append((src_val, dst_val))
    except Exception as e:
        print(f"Error extracting coordinates: {e}")
    
    return coordinates


def create_matrix_visual(coordinates: List[Tuple[int, int]], max_size: int = 8) -> VGroup:
    """
    Create a clean visual matrix representation showing only filled coordinates.
    
    Args:
        coordinates: List of (row, col) tuples to highlight
        max_size: Maximum matrix dimension to display
        
    Returns:
        VGroup containing the matrix visualization
    """
    if not coordinates:
        # Return empty 2x2 matrix
        matrix_group = VGroup()
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=0.3, color=WHITE, fill_opacity=0.1, stroke_color=GRAY)
                cell.shift(RIGHT * j * 0.35 + DOWN * i * 0.35)
                matrix_group.add(cell)
        return matrix_group
    
    # Determine actual matrix size needed
    max_coord = max(max(coord) for coord in coordinates) if coordinates else 0
    matrix_size = min(max_size, max(2, 2 ** (max_coord.bit_length())))
    
    matrix_group = VGroup()
    
    # Create grid of cells - no labels, just filled/empty
    for i in range(matrix_size):
        for j in range(matrix_size):
            if (i, j) in coordinates:
                # Filled cell
                cell = Square(side_length=0.3, color=BLUE, fill_opacity=0.8, stroke_color=WHITE)
            else:
                # Empty cell
                cell = Square(side_length=0.3, color=WHITE, fill_opacity=0.1, stroke_color=GRAY)
            
            cell.shift(RIGHT * j * 0.35 + DOWN * i * 0.35)
            matrix_group.add(cell)
    
    return matrix_group


class MatrixTrajectoryVisualization(Scene):
    """Visualize trajectories at the matrix level showing coordinate entries."""
    
    def construct(self):
        title = Text("Matrix-Level Trajectory Visualization", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Show how a single trajectory evolves at matrix level
        self.show_matrix_trajectory_evolution()
        self.wait(2)
        
        # Show side-by-side matrix evolution
        self.show_trajectory_matrix_comparison()
        self.wait(2)

    def show_matrix_trajectory_evolution(self):
        # Set curve type
        set_matrix_curve_type("morton")
        
        # Calculate trajectory
        start_node = create_matrix_graph(7)  # Use a number with interesting matrix
        trajectory = calculate_trajectory(start_node, max_steps=4)
        
        # Show matrices in sequence - clean, no text
        current_matrix = None
        for i, node in enumerate(trajectory):
            coordinates = get_matrix_entries_as_coordinates(node)
            matrix_visual = create_matrix_visual(coordinates, max_size=4)
            
            # Center the matrix
            matrix_visual.move_to(ORIGIN)
            
            if i == 0:
                # First matrix - just create it
                self.play(Create(matrix_visual), run_time=1.0)
                current_matrix = matrix_visual
            else:
                # Replace previous matrix with new one
                self.play(Transform(current_matrix, matrix_visual), run_time=1.0)
            
            self.wait(1.0)

    def show_trajectory_matrix_comparison(self):
        # Clear previous content except title
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))
        
        # Calculate trajectories for both
        start_val = 5
        
        # Morton trajectory
        set_matrix_curve_type("morton")
        morton_start = create_matrix_graph(start_val)
        morton_trajectory = calculate_trajectory(morton_start, max_steps=3)
        
        # Hilbert trajectory  
        set_matrix_curve_type("hilbert")
        hilbert_start = create_matrix_graph(start_val)
        hilbert_trajectory = calculate_trajectory(hilbert_start, max_steps=3)
        
        # Show both trajectories side by side
        self.animate_dual_matrix_trajectory(morton_trajectory, hilbert_trajectory)

    def animate_dual_matrix_trajectory(self, morton_trajectory, hilbert_trajectory):
        """Animate two trajectories side by side showing clean matrix evolution."""
        
        max_steps = max(len(morton_trajectory), len(hilbert_trajectory))
        morton_current = None
        hilbert_current = None
        
        for step in range(max_steps):
            # Morton side (left)
            if step < len(morton_trajectory):
                morton_coords = get_matrix_entries_as_coordinates(morton_trajectory[step])
                morton_matrix = create_matrix_visual(morton_coords, max_size=4)
                morton_matrix.shift(LEFT * 3)
            
            # Hilbert side (right)
            if step < len(hilbert_trajectory):
                hilbert_coords = get_matrix_entries_as_coordinates(hilbert_trajectory[step])
                hilbert_matrix = create_matrix_visual(hilbert_coords, max_size=4)
                hilbert_matrix.shift(RIGHT * 3)
            
            # Animate both appearing/transforming
            animations = []
            if step < len(morton_trajectory):
                if step == 0:
                    animations.append(Create(morton_matrix))
                    morton_current = morton_matrix
                else:
                    animations.append(Transform(morton_current, morton_matrix))
                
            if step < len(hilbert_trajectory):
                if step == 0:
                    animations.append(Create(hilbert_matrix))
                    hilbert_current = hilbert_matrix
                else:
                    animations.append(Transform(hilbert_current, hilbert_matrix))
            
            if animations:
                self.play(*animations, run_time=1.2)
            
            self.wait(0.8)


class DetailedMatrixEvolution(Scene):
    """Show detailed step-by-step matrix evolution with highlighting."""
    
    def construct(self):
        title = Text("Detailed Matrix Entry Evolution", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        self.show_detailed_evolution()
        self.wait(2)

    def show_detailed_evolution(self):
        subtitle = Text("Tracking Individual Matrix Entries", font_size=20)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))
        
        # Use Morton curve
        set_matrix_curve_type("morton")
        
        # Start with a node that has multiple entries
        start_node = create_matrix_graph(11)  # Should have interesting matrix structure
        trajectory = calculate_trajectory(start_node, max_steps=3)
        
        # Show detailed evolution
        for i, node in enumerate(trajectory):
            self.show_node_detail(node, i, len(trajectory))
            if i < len(trajectory) - 1:
                self.wait(1)
                # Clear for next step
                if i < len(trajectory) - 2:  # Don't clear on the last iteration
                    self.play(FadeOut(*[mob for mob in self.mobjects[2:]]))

    def show_node_detail(self, node, step_num, total_steps):
        """Show detailed breakdown of a single node's matrix representation."""
        
        # Step header
        step_text = Text(f"Step {step_num} of {total_steps-1}", font_size=18, color=YELLOW)
        step_text.shift(UP * 2)
        self.play(Write(step_text))
        
        # Node value
        try:
            node_val = node.to_int()
            node_text = Text(f"Node Value: {node_val}", font_size=16, color=BLUE)
        except:
            node_text = Text("Node Value: ?", font_size=16, color=BLUE)
        node_text.shift(UP * 1.5)
        self.play(Write(node_text))
        
        # Extract coordinates
        coordinates = get_matrix_entries_as_coordinates(node)
        
        # Show coordinate list
        coord_text = Text(f"Matrix Entries (row,col): {coordinates}", font_size=14, color=GREEN)
        coord_text.shift(UP * 1)
        self.play(Write(coord_text))
        
        # Create and display matrix
        matrix_visual = create_matrix_visual(coordinates, max_size=6)
        matrix_visual.shift(DOWN * 0.5)
        
        # Add matrix border
        if coordinates:
            max_coord = max(max(coord) for coord in coordinates)
            matrix_size = min(6, max(2, 2 ** (max_coord.bit_length())))
        else:
            matrix_size = 2
            
        border = Rectangle(
            width=matrix_size * 0.35 + 0.1,
            height=matrix_size * 0.35 + 0.1,
            color=WHITE
        )
        border.move_to(matrix_visual.get_center())
        
        # Animate matrix creation
        self.play(Create(border))
        self.play(Create(matrix_visual), run_time=1.5)
        
        # Highlight each entry one by one
        if coordinates:
            highlight_text = Text("Highlighting entries:", font_size=12, color=ORANGE)
            highlight_text.shift(DOWN * 2.5)
            self.play(Write(highlight_text))
            
            for i, (row, col) in enumerate(coordinates):
                # Create highlight circle
                highlight = Circle(radius=0.2, color=RED, stroke_width=4)
                highlight.shift(RIGHT * col * 0.35 + DOWN * (row * 0.35 + 0.5))
                
                entry_text = Text(f"Entry {i+1}: ({row},{col})", font_size=10, color=RED)
                entry_text.next_to(highlight_text, DOWN, buff=0.1 + i * 0.3)
                
                self.play(Create(highlight), Write(entry_text), run_time=0.8)
                self.wait(0.3)
                self.play(FadeOut(highlight), run_time=0.3)


if __name__ == "__main__":
    # To render: manim -pql matrix_trajectory_animation.py MatrixTrajectoryVisualization
    # To render: manim -pql matrix_trajectory_animation.py DetailedMatrixEvolution
    pass