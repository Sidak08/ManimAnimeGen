from manimlib import *

class PythagoreanTheoremMinimal(Scene):
    def construct(self):
        # Title
        title = Text("Pythagorean Theorem", font_size=60)
        subtitle = Text("in 30 seconds", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), run_time=1)
        self.play(Write(subtitle), run_time=0.5)
        self.wait(0.5)
        
        self.play(FadeOut(VGroup(title, subtitle)))
        
        # Create triangle
        triangle = Polygon(ORIGIN, 4*RIGHT, 4*RIGHT + 3*UP, color=WHITE)
        right_angle = Square(side_length=0.4).move_to(ORIGIN).shift(0.2*RIGHT + 0.2*UP)
        
        # Labels
        a_label = Tex("a = 3", color=BLUE)
        b_label = Tex("b = 4", color=GREEN)
        c_label = Tex("c = 5", color=RED)
        
        a_label.next_to(triangle.get_bottom(), DOWN)
        b_label.next_to(triangle.get_right(), RIGHT)
        c_label.next_to(triangle.get_center() + 0.5*UP + 0.5*LEFT)
        
        explanation = Text("In a right-angled triangle").to_edge(UP)
        
        self.play(
            ShowCreation(triangle),
            ShowCreation(right_angle),
            Write(explanation),
            run_time=1.5
        )
        
        self.play(
            Write(a_label),
            Write(b_label),
            Write(c_label),
            run_time=1
        )
        
        # Formula
        formula = Tex("a^2 + b^2 = c^2")
        formula.to_edge(DOWN, buff=1)
        
        pythagoras = Text("Pythagoras discovered:")
        pythagoras.next_to(formula, UP)
        
        self.play(
            Write(pythagoras),
            Write(formula),
            run_time=1.5
        )
        
        # Squares
        a_square = Square(side_length=3, color=BLUE)
        a_square.next_to(triangle, DOWN, buff=0.5)
        
        b_square = Square(side_length=4, color=GREEN)
        b_square.next_to(triangle, RIGHT, buff=0.5)
        
        c_square = Square(side_length=5, color=RED)
        c_square.next_to(triangle, UP + LEFT, buff=0.5)
        
        self.play(
            ShowCreation(a_square),
            ShowCreation(b_square),
            ShowCreation(c_square),
            run_time=1.5
        )
        
        # Area labels
        a_area = Tex("9", color=BLUE)
        b_area = Tex("16", color=GREEN)
        c_area = Tex("25", color=RED)
        
        a_area.move_to(a_square)
        b_area.move_to(b_square)
        c_area.move_to(c_square)
        
        self.play(
            Write(a_area),
            Write(b_area),
            Write(c_area),
            run_time=1
        )
        
        # Calculate
        calculation = Tex("9 + 16 = 25")
        calculation.next_to(formula, UP, buff=1)
        
        self.play(
            FadeOut(pythagoras),
            Write(calculation),
            run_time=1
        )
        
        # Final message
        final_message = Text("The squares on the legs\nadd up to the square on the hypotenuse!")
        final_message.to_edge(UP)
        
        self.play(
            FadeOut(explanation),
            FadeIn(final_message),
            run_time=1
        )
        
        mind_blown = Text("Mind = Blown 🤯", color=YELLOW)
        mind_blown.to_edge(DOWN)
        
        self.play(
            FadeIn(mind_blown),
            run_time=1
        )
        
        self.wait(0.5)