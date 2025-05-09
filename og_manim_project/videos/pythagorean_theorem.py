from manim_imports_ext import *

class PythagoreanTheorem(InteractiveScene):
    def construct(self):
        # Opening title
        title = Text("The Pythagorean Theorem", font_size=72)
        subtitle = Text("in 30 seconds", font_size=48, color=YELLOW)
        subtitle.next_to(title, DOWN)
        
        opening_group = VGroup(title, subtitle)
        opening_group.to_edge(UP)
        
        # Right-angled triangle with labels
        triangle = Polygon(ORIGIN, 4*RIGHT, 4*RIGHT + 3*UP, color=WHITE)
        
        # Labels for sides
        a_label = MathTex("a", font_size=48, color=BLUE)
        b_label = MathTex("b", font_size=48, color=GREEN)
        c_label = MathTex("c", font_size=48, color=RED)
        
        a_label.next_to(triangle.get_right(), DOWN)
        b_label.next_to(triangle.get_top(), RIGHT)
        c_label.move_to(triangle.get_center() + 0.5*UP + 0.5*LEFT)
        
        # Right angle symbol
        right_angle = Square(side_length=0.4).move_to(ORIGIN).shift(0.2*RIGHT + 0.2*UP)
        
        # Formula
        formula = MathTex("a^2 + b^2 = c^2", font_size=72)
        formula.to_edge(DOWN, buff=1.5)
        
        # Squares for visual demonstration
        a_square = Square(side_length=3, color=BLUE).move_to(2*LEFT + 1.5*DOWN)
        b_square = Square(side_length=4, color=GREEN).move_to(4*RIGHT + 2*DOWN)
        c_square = Square(side_length=5, color=RED).move_to(5.5*RIGHT + 4*UP)
        
        a_square_tex = MathTex("a^2 = 9", font_size=36, color=BLUE)
        b_square_tex = MathTex("b^2 = 16", font_size=36, color=GREEN)
        c_square_tex = MathTex("c^2 = 25", font_size=36, color=RED)
        
        a_square_tex.move_to(a_square)
        b_square_tex.move_to(b_square)
        c_square_tex.move_to(c_square)
        
        # Example calculation
        example = VGroup(
            MathTex("a = 3, b = 4", font_size=48),
            MathTex("3^2 + 4^2 = 9 + 16 = 25", font_size=48),
            MathTex("c^2 = 25 \\Rightarrow c = 5", font_size=48)
        )
        example.arrange(DOWN, buff=0.5)
        
        # Final message
        final_message = Text("Triangles and squares are best friends!", font_size=48)
        mind_blown = Text("Mind = Blown 🤯", font_size=72, color=YELLOW)
        
        # Animation sequence
        
        # Opening
        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP*0.5))
        self.wait(0.5)
        
        # Transition to triangle
        self.play(FadeOut(opening_group))
        
        # Draw triangle and labels
        self.play(Create(triangle))
        self.play(Create(right_angle))
        self.play(Write(a_label), Write(b_label), Write(c_label))
        
        explanation = Text("In a right-angled triangle, the sides are a, b, and c", 
                           font_size=36).to_edge(UP)
        self.play(Write(explanation))
        
        explanation2 = Text("c is the hypotenuse - the longest side", 
                           font_size=36).next_to(explanation, DOWN)
        self.play(Write(explanation2))
        self.wait(0.5)
        
        # Formula
        self.play(
            FadeOut(explanation),
            FadeOut(explanation2),
            Write(formula)
        )
        
        formula_explanation = Text("Pythagoras figured out this relationship", 
                                 font_size=36).to_edge(UP)
        
        self.play(Write(formula_explanation))
        self.wait(0.5)
        
        # Example calculation
        self.play(
            FadeOut(formula_explanation),
            FadeOut(triangle), 
            FadeOut(right_angle),
            FadeOut(a_label), 
            FadeOut(b_label), 
            FadeOut(c_label)
        )
        
        self.play(Write(example[0]))
        self.play(Write(example[1]))
        self.play(Write(example[2]))
        self.wait(0.5)
        
        # Visual demonstration with squares
        self.play(
            FadeOut(example),
            formula.animate.to_edge(UP)
        )
        
        self.play(
            Create(a_square),
            Create(b_square),
            Create(c_square)
        )
        
        self.play(
            Write(a_square_tex),
            Write(b_square_tex),
            Write(c_square_tex)
        )
        
        squares_explanation = Text("The squares built on the legs add up to the square on the hypotenuse!", 
                                font_size=30).next_to(formula, DOWN)
        self.play(Write(squares_explanation))
        self.wait(0.75)
        
        # Final message
        self.play(
            FadeOut(a_square),
            FadeOut(b_square),
            FadeOut(c_square),
            FadeOut(a_square_tex),
            FadeOut(b_square_tex),
            FadeOut(c_square_tex),
            FadeOut(squares_explanation),
            FadeOut(formula)
        )
        
        self.play(Write(final_message))
        self.wait(0.5)
        self.play(
            final_message.animate.to_edge(UP),
            FadeIn(mind_blown, scale=1.5)
        )
        self.wait(1)