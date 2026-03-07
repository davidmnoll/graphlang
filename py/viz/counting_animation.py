from manim import *
import numpy as np
from test_eval import create_matrix_graph, set_matrix_curve_type
from matrix_trajectory_animation import get_matrix_entries_as_coordinates
from typing import List, Tuple


def create_counting_matrix(coordinates: List[Tuple[int, int]], number: int, max_size: int = 8) -> VGroup:
    """
    Create matrix visualization for counting animation with number display.
    """
    if not coordinates:
        return VGroup()
    
    # Determine matrix size
    max_coord = max(max(coord) for coord in coordinates) if coordinates else 0
    matrix_size = min(max_size, max(2, 2 ** (max_coord.bit_length())))
    
    matrix_group = VGroup()
    
    # Scale cell size based on matrix size
    cell_size = max(0.12, 0.8 / matrix_size)
    spacing = cell_size + 0.02
    
    # Create clean grid
    for i in range(matrix_size):
        for j in range(matrix_size):
            if (i, j) in coordinates:
                # Filled cell - bright color
                cell = Square(side_length=cell_size, color=BLUE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
            else:
                # Empty cell - very light
                cell = Square(side_length=cell_size, color=WHITE, fill_opacity=0.03, stroke_color=GRAY, stroke_width=0.3)
            
            cell.shift(RIGHT * j * spacing + DOWN * i * spacing)
            matrix_group.add(cell)
    
    return matrix_group


class MortonCounting(Scene):
    """Count from 1 to N showing Morton curve matrix patterns."""
    
    def construct(self):
        set_matrix_curve_type("morton")
        
        # Add title
        title = Text("Morton Curve: 1 → 128", font_size=24, color=BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Count from 1 to 128
        current_matrix = None
        number_display = None
        
        for n in range(1, 129, 2):  # Skip even numbers for speed
            node = create_matrix_graph(n)
            coordinates = get_matrix_entries_as_coordinates(node)
            matrix_visual = create_counting_matrix(coordinates, n, max_size=8)
            matrix_visual.move_to(ORIGIN)
            
            # Number display
            new_number_display = Text(str(n), font_size=20, color=YELLOW)
            new_number_display.next_to(matrix_visual, DOWN, buff=0.5)
            
            if current_matrix is None:
                # First matrix
                self.play(Create(matrix_visual), Write(new_number_display), run_time=0.3)
                current_matrix = matrix_visual
                number_display = new_number_display
            else:
                # Transform to next matrix
                self.play(
                    Transform(current_matrix, matrix_visual),
                    Transform(number_display, new_number_display),
                    run_time=0.15
                )
            
            if n % 16 == 1:  # Pause occasionally to see patterns
                self.wait(0.3)


class HilbertCounting(Scene):
    """Count from 1 to N showing Hilbert curve matrix patterns."""
    
    def construct(self):
        set_matrix_curve_type("hilbert")
        
        # Add title
        title = Text("Hilbert Curve: 1 → 128", font_size=24, color=GREEN)
        title.to_edge(UP)
        self.add(title)
        
        # Count from 1 to 128
        current_matrix = None
        number_display = None
        
        for n in range(1, 129, 2):  # Skip even numbers for speed
            node = create_matrix_graph(n)
            coordinates = get_matrix_entries_as_coordinates(node)
            matrix_visual = create_counting_matrix(coordinates, n, max_size=8)
            matrix_visual.move_to(ORIGIN)
            
            # Number display - use simpler text creation
            new_number_display = Text(str(n), font_size=20)
            new_number_display.set_color(YELLOW)
            new_number_display.next_to(matrix_visual, DOWN, buff=0.5)
            
            if current_matrix is None:
                # First matrix
                self.play(Create(matrix_visual), Write(new_number_display), run_time=0.3)
                current_matrix = matrix_visual
                number_display = new_number_display
            else:
                # Transform to next matrix
                self.play(
                    Transform(current_matrix, matrix_visual),
                    Transform(number_display, new_number_display),
                    run_time=0.15
                )
            
            if n % 16 == 1:  # Pause occasionally to see patterns
                self.wait(0.3)


class DualCounting(Scene):
    """Side-by-side counting comparison of Morton vs Hilbert."""
    
    def construct(self):
        # Add titles
        morton_title = Text("Morton", font_size=20, color=BLUE)
        morton_title.shift(LEFT * 4 + UP * 3)
        
        hilbert_title = Text("Hilbert", font_size=20, color=GREEN)
        hilbert_title.shift(RIGHT * 4 + UP * 3)
        
        self.add(morton_title, hilbert_title)
        
        # Initialize
        morton_current = None
        hilbert_current = None
        morton_number = None
        hilbert_number = None
        
        for n in range(1, 129, 3):  # Every 3rd number for speed
            # Morton side
            set_matrix_curve_type("morton")
            morton_node = create_matrix_graph(n)
            morton_coords = get_matrix_entries_as_coordinates(morton_node)
            morton_matrix = create_counting_matrix(morton_coords, n, max_size=6)
            morton_matrix.shift(LEFT * 4)
            
            morton_num_display = Text(str(n), font_size=16, color=BLUE)
            morton_num_display.next_to(morton_matrix, DOWN, buff=0.3)
            
            # Hilbert side
            set_matrix_curve_type("hilbert")
            hilbert_node = create_matrix_graph(n)
            hilbert_coords = get_matrix_entries_as_coordinates(hilbert_node)
            hilbert_matrix = create_counting_matrix(hilbert_coords, n, max_size=6)
            hilbert_matrix.shift(RIGHT * 4)
            
            hilbert_num_display = Text(str(n), font_size=16, color=GREEN)
            hilbert_num_display.next_to(hilbert_matrix, DOWN, buff=0.3)
            
            if morton_current is None:
                # First matrices
                self.play(
                    Create(morton_matrix),
                    Create(hilbert_matrix),
                    Write(morton_num_display),
                    Write(hilbert_num_display),
                    run_time=0.4
                )
                morton_current = morton_matrix
                hilbert_current = hilbert_matrix
                morton_number = morton_num_display
                hilbert_number = hilbert_num_display
            else:
                # Transform to next matrices
                self.play(
                    Transform(morton_current, morton_matrix),
                    Transform(hilbert_current, hilbert_matrix),
                    Transform(morton_number, morton_num_display),
                    Transform(hilbert_number, hilbert_num_display),
                    run_time=0.1
                )
            
            # Pause at interesting numbers
            if n in [7, 15, 31, 63, 127]:
                self.wait(0.5)


class FastCounting(Scene):
    """Very fast counting to show overall patterns."""
    
    def construct(self):
        # Split screen setup
        divider = Line(UP * 4, DOWN * 4, color=WHITE, stroke_width=1)
        self.add(divider)
        
        morton_title = Text("Morton", font_size=18, color=BLUE)
        morton_title.shift(LEFT * 3 + UP * 3.5)
        
        hilbert_title = Text("Hilbert", font_size=18, color=GREEN)
        hilbert_title.shift(RIGHT * 3 + UP * 3.5)
        
        self.add(morton_title, hilbert_title)
        
        # Very fast counting
        morton_current = None
        hilbert_current = None
        
        for n in range(1, 257, 8):  # Every 8th number, very fast
            # Morton
            set_matrix_curve_type("morton")
            morton_node = create_matrix_graph(n)
            morton_coords = get_matrix_entries_as_coordinates(morton_node)
            morton_matrix = create_counting_matrix(morton_coords, n, max_size=8)
            morton_matrix.shift(LEFT * 3)
            
            # Hilbert
            set_matrix_curve_type("hilbert")
            hilbert_node = create_matrix_graph(n)
            hilbert_coords = get_matrix_entries_as_coordinates(hilbert_node)
            hilbert_matrix = create_counting_matrix(hilbert_coords, n, max_size=8)
            hilbert_matrix.shift(RIGHT * 3)
            
            if morton_current is None:
                self.play(Create(morton_matrix), Create(hilbert_matrix), run_time=0.2)
                morton_current = morton_matrix
                hilbert_current = hilbert_matrix
            else:
                self.play(
                    Transform(morton_current, morton_matrix),
                    Transform(hilbert_current, hilbert_matrix),
                    run_time=0.05
                )
            
            # Brief pause at powers of 2
            if n & (n - 1) == 0:  # Power of 2
                self.wait(0.2)


class SlowMortonCounting(Scene):
    """Slow Morton counting animation to see each step clearly."""
    
    def construct(self):
        set_matrix_curve_type("morton")
        
        # Add title as simple text
        title_text = "Morton Curve (Slow): 1 → 64"
        title = Text(title_text, font_size=24)
        title.set_color(BLUE)
        title.to_edge(UP)
        self.add(title)
        
        # Count from 1 to 64 slowly
        current_matrix = None
        
        for n in range(1, 65):  # Every number, slow
            node = create_matrix_graph(n)
            coordinates = get_matrix_entries_as_coordinates(node)
            matrix_visual = create_counting_matrix(coordinates, n, max_size=8)
            matrix_visual.move_to(ORIGIN)
            
            if current_matrix is None:
                # First matrix
                self.play(Create(matrix_visual), run_time=0.8)
                current_matrix = matrix_visual
            else:
                # Transform to next matrix
                self.play(Transform(current_matrix, matrix_visual), run_time=0.5)
            
            # Pause at powers of 2 to see patterns
            if n & (n - 1) == 0:  # Power of 2
                self.wait(1.0)
            else:
                self.wait(0.3)


class SlowHilbertCounting(Scene):
    """Slow Hilbert counting animation to see each step clearly."""
    
    def construct(self):
        set_matrix_curve_type("hilbert")
        
        # Add title
        title = Text("Hilbert Curve (Slow): 1 → 64", font_size=24, color=GREEN)
        title.to_edge(UP)
        self.add(title)
        
        # Count from 1 to 64 slowly
        current_matrix = None
        number_display = None
        
        for n in range(1, 65):  # Every number, slow
            node = create_matrix_graph(n)
            coordinates = get_matrix_entries_as_coordinates(node)
            matrix_visual = create_counting_matrix(coordinates, n, max_size=8)
            matrix_visual.move_to(ORIGIN)
            
            # Number display
            new_number_display = Text(str(n), font_size=20)
            new_number_display.set_color(YELLOW)
            new_number_display.next_to(matrix_visual, DOWN, buff=0.5)
            
            if current_matrix is None:
                # First matrix
                self.play(Create(matrix_visual), Write(new_number_display), run_time=0.8)
                current_matrix = matrix_visual
                number_display = new_number_display
            else:
                # Transform to next matrix
                self.play(
                    Transform(current_matrix, matrix_visual),
                    Transform(number_display, new_number_display),
                    run_time=0.5
                )
            
            # Pause at powers of 2 to see patterns
            if n & (n - 1) == 0:  # Power of 2
                self.wait(1.0)
            else:
                self.wait(0.3)


class HighlightDifferences(Scene):
    """Show specific numbers that highlight differences."""
    
    def construct(self):
        title = Text("Key Differences", font_size=24, color=YELLOW)
        title.to_edge(UP)
        self.add(title)
        
        # Numbers that show clear differences
        interesting_numbers = [5, 7, 9, 11, 19, 21, 23, 37, 41, 43]
        
        morton_current = None
        hilbert_current = None
        number_display = None
        
        for n in interesting_numbers:
            # Morton
            set_matrix_curve_type("morton")
            morton_node = create_matrix_graph(n)
            morton_coords = get_matrix_entries_as_coordinates(morton_node)
            morton_matrix = create_counting_matrix(morton_coords, n, max_size=6)
            morton_matrix.shift(LEFT * 3)
            
            # Hilbert
            set_matrix_curve_type("hilbert")
            hilbert_node = create_matrix_graph(n)
            hilbert_coords = get_matrix_entries_as_coordinates(hilbert_node)
            hilbert_matrix = create_counting_matrix(hilbert_coords, n, max_size=6)
            hilbert_matrix.shift(RIGHT * 3)
            
            # Number display
            num_text = Text(f"n = {n}", font_size=20)
            num_text.set_color(WHITE)
            num_text.shift(DOWN * 2.5)
            
            if morton_current is None:
                self.play(
                    Create(morton_matrix),
                    Create(hilbert_matrix),
                    Write(num_text),
                    run_time=0.8
                )
                morton_current = morton_matrix
                hilbert_current = hilbert_matrix
                number_display = num_text
            else:
                self.play(
                    Transform(morton_current, morton_matrix),
                    Transform(hilbert_current, hilbert_matrix),
                    Transform(number_display, num_text),
                    run_time=0.8
                )
            
            self.wait(1.2)  # Pause to see each difference clearly


if __name__ == "__main__":
    # To render: manim -pql counting_animation.py MortonCounting
    # To render: manim -pql counting_animation.py HilbertCounting  
    # To render: manim -pql counting_animation.py DualCounting
    # To render: manim -pql counting_animation.py FastCounting
    # To render: manim -pql counting_animation.py SlowMortonCounting
    # To render: manim -pql counting_animation.py SlowHilbertCounting
    # To render: manim -pql counting_animation.py HighlightDifferences
    pass