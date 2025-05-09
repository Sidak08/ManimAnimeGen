from manimlib import *

class PythagoreanTheorem(Scene):
    def construct(self):
        # Opening title
        title = Text("The Pythagorean Theorem", font_size=60)
        subtitle = Text("in 30 seconds", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        # Create the 3-4-5 triangle
        triangle = Polygon(
            ORIGIN, 
            4*RIGHT, 
            4*RIGHT + 3*UP, 
            color=WHITE
        )
        
        # Labels for sides
        a_label = Tex("a = 3", font_size=36, color=BLUE)
        b_label = Tex("b = 4", font_size=36, color=GREEN)
        c_label = Tex("c = 5", font_size=36, color=RED)
        
        a_label.next_to(triangle.get_bottom(), DOWN)
        b_label.next_to(triangle.get_right(), RIGHT)
        c_label.next_to(triangle.get_center() + 0.5*UP + 0.5*LEFT)
        
        # Right angle symbol
        right_angle = Square(side_length=0.4)
        right_angle.move_to(ORIGIN)
        right_angle.shift(0.2*RIGHT + 0.2*UP)
        
        # The main formula
        formula = Tex("a^2 + b^2 = c^2", font_size=60)
        formula.to_edge(DOWN, buff=1)
        
        # Create squares on each side of the triangle
        a_square = Square(side_length=3, color=BLUE)
        a_square.next_to(triangle, DOWN, buff=0.5)
        
        b_square = Square(side_length=4, color=GREEN)
        b_square.next_to(triangle, RIGHT, buff=0.5)
        
        c_square = Square(side_length=5, color=RED)
        c_square.next_to(triangle, UP + LEFT, buff=0.5)
        
        # Labels for the areas
        a_area = Tex("a^2 = 9", font_size=36, color=BLUE)
        b_area = Tex("b^2 = 16", font_size=36, color=GREEN)
        c_area = Tex("c^2 = 25", font_size=36, color=RED)
        
        a_area.move_to(a_square)
        b_area.move_to(b_square)
        c_area.move_to(c_square)
        
        # Animation Sequence
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(0.5)
        
        self.play(FadeOut(title), FadeOut(subtitle))
        
        # Draw triangle and labels
        self.play(ShowCreation(triangle))
        self.play(ShowCreation(right_angle))
        
        explanation = Text("In a right-angled triangle", font_size=36).to_edge(UP)
        self.play(Write(explanation))
        
        self.play(
            Write(a_label),
            Write(b_label), 
            Write(c_label)
        )
        self.wait(0.5)
        
        # Formula introduction
        self.play(Write(formula))
        
        # Show the squares and their areas
        self.play(
            ShowCreation(a_square),
            ShowCreation(b_square), 
            ShowCreation(c_square)
        )
        
        self.play(
            Write(a_area),
            Write(b_area),
            Write(c_area)
        )
        
        # Highlight the equation
        calculation = Tex("9 + 16 = 25", font_size=48)
        calculation.next_to(formula, UP)
        self.play(Write(calculation))
        
        # Final message
        final_message = Text("The squares on the legs\nadd up to the square on the hypotenuse!", 
                           font_size=36)
        final_message.to_edge(UP)
        
        self.play(
            FadeOut(explanation),
            FadeIn(final_message)
        )
        
        mind_blown = Text("Mind = Blown 🤯", font_size=60, color=YELLOW)
        mind_blown.to_edge(DOWN)
        
        self.play(FadeIn(mind_blown))
        self.wait(1)