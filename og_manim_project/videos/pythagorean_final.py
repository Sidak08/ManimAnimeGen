from manimlib import *

class PythagoreanTheoremExplained(Scene):
    def construct(self):
        # Opening title with more engaging text
        title = Text("The Pythagorean Theorem", font_size=72)
        subtitle = Text("Visualized in 30 Seconds", font_size=42, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        opening_group = VGroup(title, subtitle)
        opening_group.to_edge(UP)
        
        # Create a cleaner 3-4-5 triangle
        triangle = Polygon(
            ORIGIN, 
            4*RIGHT, 
            4*RIGHT + 3*UP, 
            color=WHITE,
            fill_opacity=0.2
        )
        
        # Better labels with more distinct colors
        a_side = Line(ORIGIN, 4*RIGHT, color=BLUE, stroke_width=6)
        b_side = Line(4*RIGHT, 4*RIGHT + 3*UP, color=GREEN, stroke_width=6)
        c_side = Line(4*RIGHT + 3*UP, ORIGIN, color=RED, stroke_width=6)
        
        sides = VGroup(a_side, b_side, c_side)
        
        a_label = Tex("a = 3", font_size=42, color=BLUE)
        b_label = Tex("b = 4", font_size=42, color=GREEN)
        c_label = Tex("c = 5", font_size=42, color=RED)
        
        a_label.next_to(a_side, DOWN, buff=0.3)
        b_label.next_to(b_side, RIGHT, buff=0.3)
        c_label.next_to(c_side, LEFT, buff=0.3)
        
        # Right angle symbol (improved)
        right_angle = Square(side_length=0.5, color=WHITE)
        right_angle.move_to(ORIGIN)
        right_angle.shift(0.25*RIGHT + 0.25*UP)
        
        # The formula with highlighting
        formula = Tex("a^2 + b^2 = c^2", font_size=72)
        formula.to_edge(DOWN, buff=1.2)
        
        # Create visually appealing squares on sides
        a_square = Square(side_length=3, color=BLUE, fill_opacity=0.3)
        a_square.move_to(2*RIGHT + 1.5*DOWN)
        
        b_square = Square(side_length=4, color=GREEN, fill_opacity=0.3)
        b_square.move_to(6*RIGHT + 2*UP)
        
        c_square = Square(side_length=5, color=RED, fill_opacity=0.3)
        c_square.rotate(np.arctan(3/4))
        c_square.move_to(2*RIGHT + 1.5*UP)
        
        # Area labels with clearer presentation
        a_area = Tex("a^2 = 3^2 = 9", font_size=36, color=BLUE)
        b_area = Tex("b^2 = 4^2 = 16", font_size=36, color=GREEN)
        c_area = Tex("c^2 = 5^2 = 25", font_size=36, color=RED)
        
        a_area.move_to(a_square)
        b_area.move_to(b_square)
        c_area.move_to(c_square)
        
        # Create grid patterns to visualize area
        a_grid = VGroup(*[
            Square(side_length=1, color=BLUE, fill_opacity=0.15, stroke_width=1)
            for _ in range(9)
        ])
        a_grid.arrange_in_grid(3, 3, buff=0)
        a_grid.move_to(a_square)
        
        b_grid = VGroup(*[
            Square(side_length=1, color=GREEN, fill_opacity=0.15, stroke_width=1)
            for _ in range(16)
        ])
        b_grid.arrange_in_grid(4, 4, buff=0)
        b_grid.move_to(b_square)
        
        c_grid = VGroup(*[
            Square(side_length=1, color=RED, fill_opacity=0.15, stroke_width=1)
            for _ in range(25)
        ])
        c_grid.arrange_in_grid(5, 5, buff=0)
        c_grid.rotate(np.arctan(3/4))
        c_grid.move_to(c_square)
        
        # Animation Sequence - faster paced for 30 seconds
        
        # Opening (3 seconds)
        self.play(
            Write(title),
            run_time=1
        )
        self.play(
            Write(subtitle),
            run_time=0.5
        )
        self.wait(0.5)
        
        # Transition to triangle (4 seconds)
        self.play(
            FadeOut(opening_group),
            run_time=0.5
        )
        
        intro_text = Text("In a right-angled triangle:", font_size=36)
        intro_text.to_edge(UP)
        
        self.play(
            Write(intro_text),
            ShowCreation(triangle),
            ShowCreation(right_angle),
            run_time=1
        )
        
        self.play(
            *[ShowCreation(side) for side in sides],
            run_time=1
        )
        
        self.play(
            *[Write(label) for label in [a_label, b_label, c_label]],
            run_time=1
        )
        
        # Formula introduction (4 seconds)
        formula_intro = Text("Pythagoras discovered:", font_size=36)
        formula_intro.next_to(formula, UP, buff=0.5)
        
        self.play(
            Write(formula_intro),
            Write(formula),
            run_time=1.5
        )
        
        # Visual demonstration (10 seconds)
        self.play(
            ShowCreation(a_square),
            ShowCreation(b_square), 
            ShowCreation(c_square),
            run_time=1.5
        )
        
        self.play(
            ReplacementTransform(a_square.copy(), a_grid),
            ReplacementTransform(b_square.copy(), b_grid),
            ReplacementTransform(c_square.copy(), c_grid),
            run_time=1.5
        )
        
        self.play(
            Write(a_area),
            Write(b_area),
            Write(c_area),
            run_time=1.5
        )
        
        # Highlight the calculation (4 seconds)
        calculation = Tex("9 + 16 = 25", font_size=60, color=YELLOW)
        calculation.next_to(formula, UP, buff=1)
        
        self.play(
            FadeOut(formula_intro),
            Write(calculation),
            run_time=1
        )
        
        self.play(
            calculation.animate.set_color(WHITE).scale(1.2),
            run_time=0.5
        )
        
        # Final message (5 seconds)
        final_message = Text("The squares on the legs add up to the square on the hypotenuse!", 
                           font_size=36)
        final_message.to_edge(UP)
        
        self.play(
            FadeOut(intro_text),
            FadeIn(final_message),
            run_time=1
        )
        
        mind_blown = Text("Mind = Blown 🤯", font_size=72, color=YELLOW)
        mind_blown.to_edge(DOWN, buff=1)
        
        self.play(
            FadeIn(mind_blown, scale=1.5),
            run_time=1
        )
        
        follow_text = Text("Like and follow for more quick math!", font_size=36, color=BLUE)
        follow_text.next_to(mind_blown, UP, buff=0.5)
        
        self.play(
            Write(follow_text),
            run_time=1
        )
        
        self.wait(1)