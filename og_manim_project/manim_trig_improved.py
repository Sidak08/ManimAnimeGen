from manim import *
import os

class TrigIdentityAnimation(Scene):
    def construct(self):
        # Title with better animation
        title = Text("Trigonometric Identity", font_size=60)
        title.to_edge(UP, buff=0.5)
        
        # Create unit circle with proper animation
        circle = Circle(radius=2, color=WHITE)
        axes = Axes(
            x_range=[-2.5, 2.5],
            y_range=[-2.5, 2.5],
            axis_config={"include_tip": False}
        )
        origin = Dot()
        
        # Set up at 45 degrees (π/4)
        angle = PI/4
        point = circle.point_at_angle(angle)
        dot = Dot(point, color=RED)
        
        # Lines for sin and cos
        x_line = Line(ORIGIN, [point[0], 0, 0], color=GREEN, stroke_width=5)
        y_line = Line([point[0], 0, 0], point, color=BLUE, stroke_width=5)
        radius = Line(ORIGIN, point, color=YELLOW, stroke_width=3)
        
        # Angle arc
        angle_arc = Arc(radius=0.5, angle=angle, color=YELLOW)
        angle_label = MathTex(r"\theta = 45^{\circ}", font_size=36, color=YELLOW)
        angle_label.next_to(angle_arc, RIGHT, buff=0.1)
        angle_label.shift(0.2 * UP + 0.1 * LEFT)
        
        # Labels for sin and cos
        sin_label = MathTex(r"\sin(\theta) = \frac{\sqrt{2}}{2}", font_size=36, color=BLUE)
        sin_label.next_to(y_line, RIGHT, buff=0.2)
        
        cos_label = MathTex(r"\cos(\theta) = \frac{\sqrt{2}}{2}", font_size=36, color=GREEN)
        cos_label.next_to(x_line, DOWN, buff=0.2)
        
        # Main identity
        identity = MathTex(r"\sin^2\theta + \cos^2\theta = 1", font_size=48)
        identity.to_edge(DOWN, buff=1.5)
        
        # Proof elements
        proof = MathTex(r"\left(\frac{\sqrt{2}}{2}\right)^2 + \left(\frac{\sqrt{2}}{2}\right)^2 = \frac{1}{2} + \frac{1}{2} = 1", font_size=36)
        proof.next_to(identity, UP, buff=0.5)
        
        # Animation sequence with proper animations for all elements
        
        # Step 1: Show title with character-by-character animation
        self.play(AddTextLetterByLetter(title, time_per_char=0.1))
        self.wait(0.5)
        
        # Step 2: Draw axes with growing animation
        self.play(
            DrawBorderThenFill(axes, run_time=1.5),
        )
        self.wait(0.2)
        
        # Draw circle with growing animation
        self.play(
            Create(circle, run_time=1.5),
        )
        self.wait(0.2)
        
        # Add origin point with growing animation
        self.play(
            GrowFromCenter(origin, run_time=0.5)
        )
        
        # Add Unit Circle label
        circle_label = Text("Unit Circle", font_size=36)
        circle_label.to_corner(UL)
        self.play(FadeIn(circle_label, shift=UP*0.5))
        self.wait(0.3)
        
        # Step 3: Show angle and radius with animated drawing
        self.play(
            Create(angle_arc, run_time=1),
        )
        self.play(
            Write(angle_label, run_time=0.8),
        )
        self.play(
            GrowArrow(radius, run_time=1),
        )
        self.wait(0.3)
        
        # Step 4: Show point on circle with pulsing animation
        self.play(
            GrowFromCenter(dot),
            Flash(point, color=RED, flash_radius=0.3, line_length=0.3),
        )
        self.wait(0.3)
        
        # Step 5: Show sin and cos components with growing animations
        self.play(
            GrowFromPoint(x_line, origin.get_center(), run_time=1),
        )
        self.wait(0.2)
        self.play(
            GrowFromPoint(y_line, x_line.get_end(), run_time=1),
        )
        self.wait(0.3)
        
        # Add labels with fade-in and shift animations
        self.play(
            FadeIn(sin_label, shift=RIGHT*0.3),
            FadeIn(cos_label, shift=DOWN*0.3),
        )
        self.wait(0.5)
        
        # Step 6: Show identity with write animation
        self.play(Write(identity, run_time=1))
        self.wait(0.5)
        
        # Step 7: Show proof with character-by-character animation
        self.play(AddTextLetterByLetter(proof, time_per_char=0.05))
        self.wait(0.5)
        
        # Step 8: Highlight identity with surrounding box and color change
        box = SurroundingRectangle(identity, color=YELLOW, buff=0.2)
        self.play(
            Create(box),
            identity.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(0.5)
        
        # Step 9: Final message with write animation and color transition
        final_text = Text("A fundamental identity in trigonometry", font_size=36)
        final_text.next_to(title, DOWN)
        self.play(
            Write(final_text, run_time=1),
            title.animate.set_color(BLUE),
        )
        self.wait(1)
        
        # Bonus: Pulse animation on the identity to emphasize its importance
        self.play(
            Flash(
                identity.get_center(),
                color=BLUE,
                flash_radius=1.5,
                line_length=0.6,
                num_lines=12,
                rate_func=there_and_back,
                run_time=1.5,
            )
        )
        self.wait(1)

# Run directly if script is executed
if __name__ == "__main__":
    scene = TrigIdentityAnimation()
    scene.render()