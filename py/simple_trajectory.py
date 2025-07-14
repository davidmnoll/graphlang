from manim import *
import numpy as np
from test_eval import create_matrix_graph, set_matrix_curve_type
from trajectory_animation import calculate_trajectory, node_to_coordinates


class SimpleTrajectoryDemo(Scene):
    """A simple demonstration of graph node trajectories."""
    
    def construct(self):
        title = Text("Graph Node Rewrite Trajectories", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # Show single trajectory with detailed steps
        self.show_detailed_trajectory()
        self.wait(2)

    def show_detailed_trajectory(self):
        subtitle = Text("Following the transformation of node 5", font_size=20)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))
        
        # Set to Morton curve
        set_matrix_curve_type("morton")
        
        # Calculate trajectory for node 5
        start_node = create_matrix_graph(5)
        trajectory = calculate_trajectory(start_node, max_steps=6)
        
        # Show step by step
        step_info = Text("Step 0: Starting at node 5", font_size=16)
        step_info.shift(DOWN * 1)
        self.play(Write(step_info))
        
        # Create visualization elements
        dots = VGroup()
        lines = VGroup()
        labels = VGroup()
        
        # Position the trajectory in a line for clarity
        for i, node in enumerate(trajectory):
            x = (i - len(trajectory)/2 + 0.5) * 1.5
            y = -2.5
            
            dot = Dot(point=[x, y, 0], color=BLUE, radius=0.12)
            dots.add(dot)
            
            # Add label with node value
            try:
                node_val = node.to_int()
                label = Text(str(node_val), font_size=14, color=WHITE)
                label.next_to(dot, UP, buff=0.2)
                labels.add(label)
            except:
                label = Text("?", font_size=14, color=WHITE)
                label.next_to(dot, UP, buff=0.2)
                labels.add(label)
            
            # Connect to previous dot
            if i > 0:
                line = Arrow(dots[i-1].get_center(), dot.get_center(), 
                           color=YELLOW, buff=0.1, stroke_width=3)
                lines.add(line)
        
        # Animate step by step
        for i in range(len(trajectory)):
            # Update step info
            if i > 0:
                try:
                    val = trajectory[i].to_int()
                    new_step_info = Text(f"Step {i}: Transformed to node {val}", font_size=16)
                except:
                    new_step_info = Text(f"Step {i}: Transformation applied", font_size=16)
                new_step_info.shift(DOWN * 1)
                self.play(Transform(step_info, new_step_info))
            
            # Show dot and label
            self.play(Create(dots[i]), Write(labels[i]), run_time=0.8)
            
            # Show arrow to next step
            if i < len(lines):
                self.play(Create(lines[i]), run_time=0.6)
        
        # Show final summary
        self.wait(1)
        summary = Text(f"Trajectory length: {len(trajectory)} steps", font_size=16, color=GREEN)
        summary.shift(DOWN * 3.5)
        self.play(Write(summary))
        
        # Show trajectory values
        values = [node.to_int() for node in trajectory]
        value_text = Text(f"Values: {' → '.join(map(str, values))}", font_size=14, color=YELLOW)
        value_text.shift(DOWN * 4)
        self.play(Write(value_text))


class CompareRewriteRules(Scene):
    """Compare trajectories with different rewrite rules."""
    
    def construct(self):
        title = Text("Comparing Different Configurations", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        self.show_curve_comparison()
        self.wait(2)

    def show_curve_comparison(self):
        subtitle = Text("Morton vs Hilbert curves starting from node 7", font_size=20)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))
        
        # Morton trajectory
        set_matrix_curve_type("morton")
        morton_start = create_matrix_graph(7)
        morton_trajectory = calculate_trajectory(morton_start, max_steps=4)
        
        # Hilbert trajectory
        set_matrix_curve_type("hilbert")
        hilbert_start = create_matrix_graph(7)
        hilbert_trajectory = calculate_trajectory(hilbert_start, max_steps=4)
        
        # Display both trajectories
        morton_label = Text("Morton Curve:", font_size=16, color=BLUE)
        morton_label.shift(LEFT * 3 + DOWN * 1.5)
        self.play(Write(morton_label))
        
        hilbert_label = Text("Hilbert Curve:", font_size=16, color=GREEN)
        hilbert_label.shift(RIGHT * 3 + DOWN * 1.5)
        self.play(Write(hilbert_label))
        
        # Show trajectories as text for simplicity
        morton_values = [node.to_int() for node in morton_trajectory]
        hilbert_values = [node.to_int() for node in hilbert_trajectory]
        
        morton_text = Text(" → ".join(map(str, morton_values)), font_size=14, color=BLUE)
        morton_text.next_to(morton_label, DOWN, buff=0.3)
        
        hilbert_text = Text(" → ".join(map(str, hilbert_values)), font_size=14, color=GREEN)
        hilbert_text.next_to(hilbert_label, DOWN, buff=0.3)
        
        self.play(Write(morton_text), Write(hilbert_text))
        
        # Highlight differences
        if morton_values != hilbert_values:
            diff_text = Text("Different trajectories!", font_size=16, color=RED)
            diff_text.shift(DOWN * 3)
            self.play(Write(diff_text))
        else:
            same_text = Text("Same trajectory!", font_size=16, color=YELLOW)
            same_text.shift(DOWN * 3)
            self.play(Write(same_text))


if __name__ == "__main__":
    # To render: manim -pql simple_trajectory.py SimpleTrajectoryDemo
    # To render: manim -pql simple_trajectory.py CompareRewriteRules
    pass