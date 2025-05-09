from manim_imports_ext import *

class PythagoreanTheoremEnhanced(InteractiveScene):
    def construct(self):
        # Opening title
        title = Text("The Pythagorean Theorem", font_size=72)
        subtitle = Text("in 30 seconds", font_size=48, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        opening_group = VGroup(title, subtitle)
        opening_group.to_edge(UP)
        
        # Create the 3-4-5 triangle
        triangle = Polygon(
            ORIGIN, 
            4*RIGHT, 
            4*RIGHT + 3*UP, 
            color=WHITE,
            fill_opacity=0.2
        )
        
        # Labels for sides
        a_label = MathTex("a = 3", font_size=42, color=BLUE)
        b_label = MathTex("b = 4", font_size=42, color=GREEN)
        c_label = MathTex("c = 5", font_size=42, color=RED)
        
        a_label.next_to(triangle.get_bottom(), DOWN, buff=0.3)
        b_label.next_to(triangle.get_right(), RIGHT, buff=0.3)
        c_label.next_to(triangle.get_center() + 0.5*UP + 0.5*LEFT)
        
        # Right angle symbol
        right_angle = Square(side_length=0.4)
        right_angle.move_to(ORIGIN)
        right_angle.shift(0.2*RIGHT + 0.2*UP)
        
        # The main formula
        formula = MathTex("a^2 + b^2 = c^2", font_size=72)
        
        # Create squares on each side of the triangle
        a_square = Square(side_length=3, color=BLUE, fill_opacity=0.3)
        a_square.move_to(ORIGIN + 1.5*DOWN + 1.5*RIGHT)
        
        b_square = Square(side_length=4, color=GREEN, fill_opacity=0.3)
        b_square.move_to(4*RIGHT + 2*UP)
        
        c_square = Square(side_length=5, color=RED, fill_opacity=0.3)
        c_square.rotate(np.arctan(3/4))
        c_square.move_to(2*RIGHT + 1.5*UP)
        
        # Labels for the areas
        a_area = MathTex("a^2 = 9", font_size=36, color=BLUE)
        b_area = MathTex("b^2 = 16", font_size=36, color=GREEN)
        c_area = MathTex("c^2 = 25", font_size=36, color=RED)
        
        a_area.move_to(a_square)
        b_area.move_to(b_square)
        c_area.move_to(c_square)
        
        # Create area demonstration with grid patterns
        a_grid = VGroup(*[
            Square(side_length=1, color=BLUE, fill_opacity=0.2)
            for _ in range(9)
        ])
        a_grid.arrange_in_grid(3, 3, buff=0)
        a_grid.move_to(a_square)
        
        b_grid = VGroup(*[
            Square(side_length=1, color=GREEN, fill_opacity=0.2)
            for _ in range(16)
        ])
        b_grid.arrange_in_grid(4, 4, buff=0)
        b_grid.move_to(b_square)
        
        c_grid = VGroup(*[
            Square(side_length=1, color=RED, fill_opacity=0.2)
            for _ in range(25)
        ])
        c_grid.arrange_in_grid(5, 5, buff=0)
        c_grid.rotate(np.arctan(3/4))
        c_grid.move_to(c_square)
        
        # Animation Sequence
        
        # Opening
        self.play(
            Write(title),
            run_time=1
        )
        self.play(
            FadeIn(subtitle, shift=UP*0.5),
            run_time=0.5
        )
        self.wait(0.5)
        
        # Transition to triangle
        self.play(
            FadeOut(opening_group),
            run_time=0.5
        )
        
        # Draw triangle and labels
        self.play(
            Create(triangle),
            run_time=1
        )
        self.play(
            Create(right_angle),
            run_time=0.5
        )
        
        explanation = Text("In a right-angled triangle, the sides are:", 
                          font_size=36).to_edge(UP)
        self.play(
            Write(explanation),
            run_time=1
        )
        
        self.play(
            Write(a_label),
            Write(b_label), 
            Write(c_label),
            run_time=1
        )
        
        # Formula introduction
        formula.to_edge(DOWN, buff=1)
        self.play(
            Write(formula),
            run_time=1
        )
        
        pythagoras_note = Text("Pythagoras discovered:", font_size=36)
        pythagoras_note.next_to(formula, UP)
        self.play(
            Write(pythagoras_note),
            run_time=1
        )
        
        # Show the squares
        self.play(
            Create(a_square),
            Create(b_square), 
            Create(c_square),
            run_time=1.5
        )
        
        # Show calculation with grids
        self.play(
            Transform(a_square, a_grid),
            Transform(b_square, b_grid),
            Transform(c_square, c_grid),
            run_time=1.5
        )
        
        self.play(
            Write(a_area),
            Write(b_area),
            Write(c_area),
            run_time=1
        )
        
        # Highlight the equation
        calculation = MathTex("9 + 16 = 25", font_size=48)
        calculation.next_to(formula, UP)
        self.play(
            FadeOut(pythagoras_note),
            Write(calculation),
            run_time=1
        )
        
        # Visual demonstration - grid units combining
        self.play(
            FadeOut(a_area),
            FadeOut(b_area),
            FadeOut(c_area),
            run_time=0.5
        )
        
        a_grid_copy = a_grid.copy()
        b_grid_copy = b_grid.copy()
        
        self.play(
            a_grid_copy.animate.next_to(c_grid, LEFT, buff=0.5),
            b_grid_copy.animate.next_to(c_grid, RIGHT, buff=0.5),
            run_time=1.5
        )
        
        equals_sign = MathTex("=", font_size=72)
        equals_sign.move_to((a_grid_copy.get_right() + b_grid_copy.get_left())/2)
        
        self.play(
            Write(equals_sign),
            run_time=0.5
        )
        
        # Final message
        self.play(
            FadeOut(triangle),
            FadeOut(right_angle),
            FadeOut(a_label),
            FadeOut(b_label),
            FadeOut(c_label),
            FadeOut(a_square),
            FadeOut(b_square),
            FadeOut(c_square),
            FadeOut(a_grid_copy),
            FadeOut(b_grid_copy),
            FadeOut(c_grid),
            FadeOut(equals_sign),
            FadeOut(calculation),
            FadeOut(explanation),
            formula.animate.to_edge(UP),
            run_time=1
        )
        
        final_message = Text("The squares built on the legs\nadd up to the square on the hypotenuse!", 
                           font_size=36)
        final_message.next_to(formula, DOWN, buff=1)
        
        self.play(
            Write(final_message),
            run_time=1
        )
        
        mind_blown = Text("Mind = Blown 🤯", font_size=72, color=YELLOW)
        mind_blown.to_edge(DOWN, buff=1)
        
        self.play(
            FadeIn(mind_blown, scale=1.5),
            run_time=1
        )
        self.wait(1)