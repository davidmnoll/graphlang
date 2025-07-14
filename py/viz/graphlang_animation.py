from manim import *
import numpy as np


class GraphLangExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Programs as Matrices", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Part 1: Traditional Syntax Tree
        self.show_syntax_tree()
        self.wait(2)

        # Part 2: Node Representation
        self.show_node_representation()
        self.wait(2)

        # Part 3: Graph Evolution
        self.show_graph_evolution()
        self.wait(2)

        # Part 4: Matrix Representation
        self.show_matrix_representation()
        self.wait(2)

    def show_syntax_tree(self):
        # Clear previous content
        self.play(FadeOut(*[mob for mob in self.mobjects if mob != self.mobjects[0]]))

        subtitle = Text("Traditional Programming: Syntax Trees", font_size=24)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Create a simple syntax tree
        root = Circle(radius=0.3, color=BLUE).shift(LEFT * 1.5)
        root_label = Text("apply", font_size=16).move_to(root.get_center())

        left_child = Circle(radius=0.3, color=GREEN).shift(RIGHT * 1.5).shift(UP * 1)
        left_label = Text("func", font_size=16).move_to(left_child.get_center())

        right_child = (
            Circle(radius=0.3, color=YELLOW).shift(RIGHT * 1.5).shift(DOWN * 1)
        )
        right_label = Text("args", font_size=16).move_to(right_child.get_center())

        # Connect nodes
        line1 = Line(root.get_bottom(), left_child.get_top())
        line2 = Line(root.get_bottom(), right_child.get_top())

        tree_group = VGroup(
            root,
            root_label,
            left_child,
            left_label,
            right_child,
            right_label,
            line1,
            line2,
        )

        self.play(Create(tree_group))

        # Add explanation
        explanation = Text(
            "Fixed structure: operation on left, data on right", font_size=18
        ).next_to(tree_group, DOWN, buff=1)
        self.play(Write(explanation))

        return tree_group, explanation

    def show_node_representation(self):
        # Clear and set up
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))

        subtitle = Text("New Approach: Graph Nodes", font_size=24)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Show node structure N1: [N1.1L, N1.1R]
        node_text = Text("N1: [N1.1L, N1.1R]", font_size=20, color=BLUE)
        node_text.shift(UP * 0.5)
        self.play(Write(node_text))

        # Create visual representation
        left_box = Rectangle(width=1.5, height=0.8, color=GREEN).shift(LEFT * 2)
        left_label = Text("N1.1L", font_size=16).move_to(left_box.get_center())

        right_box = Rectangle(width=1.5, height=0.8, color=YELLOW).shift(RIGHT * 2)
        right_label = Text("N1.1R", font_size=16).move_to(right_box.get_center())

        arrow = Arrow(left_box.get_right(), right_box.get_left(), color=WHITE)

        node_group = VGroup(left_box, left_label, right_box, right_label, arrow)
        node_group.shift(DOWN * 0.5)

        self.play(Create(node_group))

        # Key insight
        insight = Text(
            "Key: Both left AND right can be graphs!", font_size=18, color=RED
        )
        insight.next_to(node_group, DOWN, buff=1)
        self.play(Write(insight))

        return node_group, insight

    def show_graph_evolution(self):
        # Clear and set up
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))

        subtitle = Text("Building Up From Primitives", font_size=24)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Show evolution stages
        stages = [
            ("0 - Empty: {}", BLUE),
            ("0_0 - Unit: {({}, {})}", GREEN),
            ("0_1: {({}, {({}, {})})}", YELLOW),
            ("1_0: {(({}, {}), {})}", ORANGE),
            ("1_1: Complex combinations...", RED),
        ]

        stage_group = VGroup()
        for i, (stage_text, color) in enumerate(stages):
            text = Text(stage_text, font_size=16, color=color)
            text.shift(UP * (1.5 - i * 0.6))
            stage_group.add(text)

        # Animate each stage appearing
        for text in stage_group:
            self.play(Write(text))
            self.wait(0.5)

        # Add explanation
        explanation = Text(
            "Each level builds on previous, creating infinite possibilities",
            font_size=16,
        ).next_to(stage_group, DOWN, buff=1)
        self.play(Write(explanation))

        return stage_group, explanation

    def show_matrix_representation(self):
        # Clear and set up
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))

        subtitle = Text("Matrix Representation: Nodes as Numbers", font_size=24)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Create example matrix
        matrix_text = Text("Example: 0_0-0_1-1_1", font_size=18)
        matrix_text.shift(UP * 1.5)
        self.play(Write(matrix_text))

        # Create matrix visualization
        matrix_data = [[1, 1], [0, 1]]
        matrix = Matrix(matrix_data, element_alignment_corner=[x for x in ORIGIN])
        matrix.shift(UP * 0.2)

        # Add row/column labels
        row_labels = VGroup(
            Text("0", font_size=14).next_to(matrix.get_rows()[0], LEFT),
            Text("1", font_size=14).next_to(matrix.get_rows()[1], LEFT),
        )

        col_labels = VGroup(
            Text("0", font_size=14).next_to(matrix.get_columns()[0], UP),
            Text("1", font_size=14).next_to(matrix.get_columns()[1], UP),
        )

        self.play(Create(matrix))
        self.play(Write(row_labels), Write(col_labels))

        # Key insight about matrix properties
        insight1 = Text(
            "Each node becomes both an integer AND a matrix", font_size=16, color=BLUE
        )
        insight1.next_to(matrix, DOWN, buff=0.8)

        insight2 = Text("Matrix size: 2^(2^n) for depth n", font_size=16, color=GREEN)
        insight2.next_to(insight1, DOWN, buff=0.3)

        insight3 = Text(
            "Corresponds to boolean functions on n bits!", font_size=16, color=RED
        )
        insight3.next_to(insight2, DOWN, buff=0.3)

        self.play(Write(insight1))
        self.wait(1)
        self.play(Write(insight2))
        self.wait(1)
        self.play(Write(insight3))

        return matrix, row_labels, col_labels, insight1, insight2, insight3


class MatrixEvolution(Scene):
    def construct(self):
        title = Text("Matrix Evolution and Computational Properties", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Show how matrices grow
        self.show_matrix_growth()
        self.wait(2)

        # Show computational connections
        self.show_computational_connections()
        self.wait(2)

    def show_matrix_growth(self):
        subtitle = Text("Growing Complexity", font_size=24)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Show progression of matrix sizes
        sizes = ["2×2", "4×4", "16×16", "65536×65536"]
        depths = ["n=1", "n=2", "n=3", "n=4"]

        progression = VGroup()
        for i, (size, depth) in enumerate(zip(sizes, depths)):
            size_text = Text(size, font_size=18, color=BLUE)
            depth_text = Text(depth, font_size=14, color=GRAY)

            group = VGroup(size_text, depth_text)
            group.arrange(DOWN, buff=0.2)
            group.shift(LEFT * 4 + RIGHT * i * 2.5)
            progression.add(group)

        # Add arrows between them
        arrows = VGroup()
        for i in range(len(sizes) - 1):
            arrow = Arrow(
                progression[i].get_right(),
                progression[i + 1].get_left(),
                buff=0.2,
                color=YELLOW,
            )
            arrows.add(arrow)

        self.play(Create(progression))
        self.play(Create(arrows))

        # Exponential growth warning
        warning = Text("Exponential explosion: 2^(2^n)", font_size=16, color=RED)
        warning.next_to(progression, DOWN, buff=1)
        self.play(Write(warning))

    def show_computational_connections(self):
        # Clear previous
        self.play(FadeOut(*[mob for mob in self.mobjects[1:]]))

        subtitle = Text("Computational Insights", font_size=24)
        subtitle.next_to(self.mobjects[0], DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Key connections
        connections = [
            "Diagonal = self-reference patterns",
            "Pascal's triangle structure emerges",
            "Linear transformations ↔ Complex numbers",
            "Potential connection to Gaussian integers",
            "Prime factorization for rewrite rules",
        ]

        connection_group = VGroup()
        for i, conn in enumerate(connections):
            text = Text(conn, font_size=16, color=[BLUE, GREEN, YELLOW, ORANGE, RED][i])
            text.shift(UP * (1.5 - i * 0.6))
            connection_group.add(text)

        for text in connection_group:
            self.play(Write(text))
            self.wait(0.8)

        # Final insight
        final = Text(
            "A new mathematical foundation for computation!", font_size=20, color=GOLD
        )
        final.next_to(connection_group, DOWN, buff=1)
        self.play(Write(final))


if __name__ == "__main__":
    # To render: manim -pql graphlang_animation.py GraphLangExplanation
    # To render HD: manim -pqh graphlang_animation.py GraphLangExplanation
    pass
