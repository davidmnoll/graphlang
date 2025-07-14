from manim import *
import numpy as np
from test_eval import create_matrix_graph, create_functional_node, set_matrix_curve_type, set_rewrite_rules_type, Z
from typing import List, Tuple, Optional
import math


def calculate_trajectory(start_node, max_steps: int = 10) -> List:
    """
    Calculate the trajectory of a node through rewrite transformations.
    
    Args:
        start_node: Initial node to start trajectory from
        max_steps: Maximum number of transformation steps
        
    Returns:
        List of nodes representing the trajectory
    """
    trajectory = [start_node]
    current = start_node
    
    for step in range(max_steps):
        try:
            # Apply rewrite transformation
            next_node = current.rewrite()
            
            # If no change, we've reached a fixed point
            if next_node == current:
                break
                
            trajectory.append(next_node)
            current = next_node
            
        except Exception as e:
            # If transformation fails, stop here
            print(f"Trajectory stopped at step {step}: {e}")
            break
    
    return trajectory


def node_to_coordinates(node, max_value: int = 100) -> Tuple[float, float]:
    """
    Convert a node to 2D coordinates for visualization.
    
    Args:
        node: The graph node to convert
        max_value: Maximum expected integer value for scaling
        
    Returns:
        (x, y) coordinates for the node
    """
    try:
        # Get integer representation
        int_val = node.to_int()
        
        # Scale to reasonable coordinate space
        if int_val == 0:
            return (0, 0)
        
        # Use a spiral layout based on integer value
        angle = math.log(int_val + 1) * 2 * math.pi
        radius = math.sqrt(int_val) * 0.5
        
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        return (x, y)
        
    except Exception:
        # For functional nodes or errors, use random position
        return (np.random.uniform(-3, 3), np.random.uniform(-3, 3))


class TrajectoryVisualization(Scene):
    def construct(self):
        title = Text("Graph Node Trajectories", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Show trajectory for different curve types
        self.show_morton_trajectory()
        self.wait(2)
        
        self.show_hilbert_trajectory()
        self.wait(2)
        
        self.show_comparison()
        self.wait(2)

    def show_morton_trajectory(self):
        # Clear previous content except title
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))
        
        subtitle = Text("Morton Curve Trajectory", font_size=24, color=BLUE)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))
        
        # Set to Morton curve
        set_matrix_curve_type("morton")
        
        # Create starting points
        start_values = [1, 2, 3, 5, 7]
        trajectories = []
        
        for val in start_values:
            start_node = create_matrix_graph(val)
            trajectory = calculate_trajectory(start_node, max_steps=5)
            trajectories.append(trajectory)
        
        # Visualize trajectories
        self.animate_trajectories(trajectories, color=BLUE, y_offset=0.5)

    def show_hilbert_trajectory(self):
        # Clear previous content except title
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))
        
        subtitle = Text("Hilbert Curve Trajectory", font_size=24, color=GREEN)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))
        
        # Set to Hilbert curve
        set_matrix_curve_type("hilbert")
        
        # Create starting points
        start_values = [1, 2, 3, 5, 7]
        trajectories = []
        
        for val in start_values:
            start_node = create_matrix_graph(val)
            trajectory = calculate_trajectory(start_node, max_steps=5)
            trajectories.append(trajectory)
        
        # Visualize trajectories
        self.animate_trajectories(trajectories, color=GREEN, y_offset=0.5)

    def show_comparison(self):
        # Clear previous content except title
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))
        
        subtitle = Text("Morton vs Hilbert Comparison", font_size=24, color=YELLOW)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))
        
        # Split screen comparison
        morton_label = Text("Morton", font_size=18, color=BLUE).shift(LEFT * 3 + UP * 2)
        hilbert_label = Text("Hilbert", font_size=18, color=GREEN).shift(RIGHT * 3 + UP * 2)
        
        self.play(Write(morton_label), Write(hilbert_label))
        
        # Show trajectories side by side
        start_val = 5
        
        # Morton trajectory
        set_matrix_curve_type("morton")
        morton_start = create_matrix_graph(start_val)
        morton_trajectory = calculate_trajectory(morton_start, max_steps=5)
        
        # Hilbert trajectory
        set_matrix_curve_type("hilbert")
        hilbert_start = create_matrix_graph(start_val)
        hilbert_trajectory = calculate_trajectory(hilbert_start, max_steps=5)
        
        # Animate both side by side
        self.animate_trajectory_comparison(morton_trajectory, hilbert_trajectory)

    def animate_trajectories(self, trajectories: List[List], color=BLUE, y_offset=0):
        """Animate multiple trajectories."""
        all_dots = VGroup()
        all_lines = VGroup()
        all_labels = VGroup()
        
        for i, trajectory in enumerate(trajectories):
            if len(trajectory) < 2:
                continue
                
            # Create dots for each point in trajectory
            dots = VGroup()
            lines = VGroup()
            labels = VGroup()
            
            for j, node in enumerate(trajectory):
                x, y = node_to_coordinates(node)
                # Offset each trajectory slightly
                x += (i - len(trajectories)/2) * 0.3
                y += y_offset
                
                dot = Dot(point=[x, y, 0], color=color, radius=0.08)
                dots.add(dot)
                
                # Add label with integer value
                try:
                    label = Text(str(node.to_int()), font_size=10).next_to(dot, UP, buff=0.1)
                    labels.add(label)
                except:
                    label = Text("?", font_size=10).next_to(dot, UP, buff=0.1)
                    labels.add(label)
                
                # Connect to previous point
                if j > 0:
                    line = Line(dots[j-1].get_center(), dot.get_center(), color=color, stroke_width=2)
                    lines.add(line)
            
            all_dots.add(dots)
            all_lines.add(lines)
            all_labels.add(labels)
        
        # Animate the creation of trajectories
        for i in range(len(trajectories)):
            if i < len(all_dots):
                self.play(Create(all_dots[i]), run_time=0.5)
                self.play(Write(all_labels[i]), run_time=0.3)
                if i < len(all_lines):
                    self.play(Create(all_lines[i]), run_time=0.5)

    def animate_trajectory_comparison(self, morton_trajectory, hilbert_trajectory):
        """Animate comparison of Morton vs Hilbert trajectories."""
        
        # Morton side (left)
        morton_dots = VGroup()
        morton_lines = VGroup()
        morton_labels = VGroup()
        
        for i, node in enumerate(morton_trajectory):
            x, y = node_to_coordinates(node)
            x -= 3  # Shift to left side
            y *= 0.5  # Scale down
            
            dot = Dot(point=[x, y, 0], color=BLUE, radius=0.1)
            morton_dots.add(dot)
            
            try:
                label = Text(str(node.to_int()), font_size=12).next_to(dot, UP, buff=0.1)
                morton_labels.add(label)
            except:
                label = Text("?", font_size=12).next_to(dot, UP, buff=0.1)
                morton_labels.add(label)
            
            if i > 0:
                line = Line(morton_dots[i-1].get_center(), dot.get_center(), color=BLUE, stroke_width=3)
                morton_lines.add(line)
        
        # Hilbert side (right)
        hilbert_dots = VGroup()
        hilbert_lines = VGroup()
        hilbert_labels = VGroup()
        
        for i, node in enumerate(hilbert_trajectory):
            x, y = node_to_coordinates(node)
            x += 3  # Shift to right side
            y *= 0.5  # Scale down
            
            dot = Dot(point=[x, y, 0], color=GREEN, radius=0.1)
            hilbert_dots.add(dot)
            
            try:
                label = Text(str(node.to_int()), font_size=12).next_to(dot, UP, buff=0.1)
                hilbert_labels.add(label)
            except:
                label = Text("?", font_size=12).next_to(dot, UP, buff=0.1)
                hilbert_labels.add(label)
            
            if i > 0:
                line = Line(hilbert_dots[i-1].get_center(), dot.get_center(), color=GREEN, stroke_width=3)
                hilbert_lines.add(line)
        
        # Animate both trajectories simultaneously
        max_len = max(len(morton_trajectory), len(hilbert_trajectory))
        
        for i in range(max_len):
            animations = []
            
            if i < len(morton_dots):
                animations.append(Create(morton_dots[i]))
            if i < len(hilbert_dots):
                animations.append(Create(hilbert_dots[i]))
                
            if animations:
                self.play(*animations, run_time=0.4)
            
            # Add labels
            label_animations = []
            if i < len(morton_labels):
                label_animations.append(Write(morton_labels[i]))
            if i < len(hilbert_labels):
                label_animations.append(Write(hilbert_labels[i]))
                
            if label_animations:
                self.play(*label_animations, run_time=0.2)
            
            # Add lines
            line_animations = []
            if i > 0:
                if i-1 < len(morton_lines):
                    line_animations.append(Create(morton_lines[i-1]))
                if i-1 < len(hilbert_lines):
                    line_animations.append(Create(hilbert_lines[i-1]))
                    
            if line_animations:
                self.play(*line_animations, run_time=0.3)


class InteractiveTrajectories(Scene):
    """Scene for exploring trajectories with different parameters."""
    
    def construct(self):
        title = Text("Interactive Trajectory Explorer", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create parameter controls visualization
        self.show_parameter_controls()
        self.wait(1)
        
        # Show different starting points
        self.explore_starting_points()
        self.wait(2)

    def show_parameter_controls(self):
        subtitle = Text("Parameters:", font_size=20)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))
        
        # Parameter display
        curve_text = Text("Curve Type: Morton", font_size=16, color=BLUE)
        curve_text.next_to(subtitle, DOWN, buff=0.3).shift(LEFT * 2)
        
        rewrite_text = Text("Rewrite Rules: Default", font_size=16, color=GREEN)
        rewrite_text.next_to(curve_text, DOWN, buff=0.2)
        
        start_text = Text("Starting Points: [1, 2, 3, 5, 8]", font_size=16, color=YELLOW)
        start_text.next_to(rewrite_text, DOWN, buff=0.2)
        
        self.play(Write(curve_text), Write(rewrite_text), Write(start_text))

    def explore_starting_points(self):
        # Show how different starting points lead to different trajectories
        starting_points = [1, 2, 3, 5, 8, 13]
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        
        # Set curve type
        set_matrix_curve_type("morton")
        
        all_trajectories = VGroup()
        
        for i, start_val in enumerate(starting_points):
            start_node = create_matrix_graph(start_val)
            trajectory = calculate_trajectory(start_node, max_steps=4)
            
            # Create visual trajectory
            dots = VGroup()
            lines = VGroup()
            
            for j, node in enumerate(trajectory):
                x, y = node_to_coordinates(node, max_value=50)
                # Spread out the trajectories
                x *= 0.8
                y *= 0.8
                y -= 1.5  # Move down from parameters
                
                dot = Dot(point=[x, y, 0], color=colors[i % len(colors)], radius=0.06)
                dots.add(dot)
                
                if j > 0:
                    line = Line(dots[j-1].get_center(), dot.get_center(), 
                              color=colors[i % len(colors)], stroke_width=2)
                    lines.add(line)
            
            trajectory_group = VGroup(dots, lines)
            all_trajectories.add(trajectory_group)
            
            # Animate this trajectory
            self.play(Create(dots), run_time=0.5)
            if len(lines) > 0:
                self.play(Create(lines), run_time=0.5)
        
        # Add legend
        legend_title = Text("Starting Points:", font_size=14).shift(DOWN * 2.5 + LEFT * 3)
        self.play(Write(legend_title))
        
        legend_items = VGroup()
        for i, start_val in enumerate(starting_points):
            color_dot = Dot(color=colors[i % len(colors)], radius=0.05)
            value_text = Text(str(start_val), font_size=12)
            item = VGroup(color_dot, value_text).arrange(RIGHT, buff=0.1)
            item.shift(DOWN * 2.5 + LEFT * 2 + RIGHT * i * 0.8)
            legend_items.add(item)
        
        self.play(Create(legend_items), run_time=1)


if __name__ == "__main__":
    # To render: manim -pql trajectory_animation.py TrajectoryVisualization
    # To render HD: manim -pqh trajectory_animation.py TrajectoryVisualization
    # Interactive version: manim -pql trajectory_animation.py InteractiveTrajectories
    pass