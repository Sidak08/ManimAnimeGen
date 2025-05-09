from manimlib import *

class TrigIdentity10Seconds(Scene):
    def construct(self):
        # Create a simple, fast-paced demonstration of sin²θ + cos²θ = 1
        
        # Title with identity
        identity = Tex("\\sin^2\\theta + \\cos^2\\theta = 1", font_size=72)
        identity.to_edge(UP, buff=0.5)
        
        # Unit circle
        circle = Circle(radius=2, color=WHITE)
        origin = Dot(ORIGIN, color=WHITE)
        
        # Point on circle at 45 degrees (easy to visualize)
        angle = 45 * DEGREES
        point = circle.point_at_angle(angle)
        dot = Dot(point, color=RED)
        
        # Lines for sin and cos
        x_line = Line(ORIGIN, [point[0], 0, 0], color=GREEN, stroke_width=6)
        y_line = Line([point[0], 0, 0], point, color=BLUE, stroke_width=6)
        radius_line = Line(ORIGIN, point, color=YELLOW, stroke_width=4)
        
        # Labels
        cos_label = Tex("\\cos\\theta", font_size=36, color=GREEN)
        cos_label.next_to(x_line, DOWN, buff=0.2)
        
        sin_label = Tex("\\sin\\theta", font_size=36, color=BLUE)
        sin_label.next_to(y_line, RIGHT, buff=0.2)
        
        radius_label = Tex("1", font_size=36, color=YELLOW)
        radius_label.next_to(radius_line.get_center(), UP+RIGHT, buff=0.1)
        
        # Angle arc and label
        angle_arc = Arc(radius=0.7, angle=angle, color=YELLOW)
        theta = Tex("\\theta", font_size=42, color=YELLOW)
        theta.move_to([0.4, 0.3, 0])
        
        # Equation steps
        step1 = Tex("\\sin^2\\theta + \\cos^2\\theta = ?", font_size=48)
        step1.to_edge(DOWN, buff=1.5)
        
        step2 = Tex("\\sin^2\\theta + \\cos^2\\theta = 1", font_size=48)
        step2.to_edge(DOWN, buff=1.5)
        
        # Animation sequence - 10 seconds total
        
        # Show identity (2 seconds)
        self.play(Write(identity), run_time=1)
        
        # Set up unit circle (3 seconds)
        self.play(
            ShowCreation(circle),
            ShowCreation(origin),
            run_time=1
        )
        
        self.play(
            ShowCreation(angle_arc),
            Write(theta),
            ShowCreation(radius_line),
            Write(radius_label),
            run_time=1
        )
        
        # Show point on circle and components (3 seconds)
        self.play(
            ShowCreation(dot),
            ShowCreation(x_line),
            ShowCreation(y_line),
            run_time=1
        )
        
        self.play(
            Write(cos_label),
            Write(sin_label),
            run_time=1
        )
        
        # Show equation (2 seconds)
        self.play(
            Write(step1),
            run_time=0.5
        )
        
        self.play(
            ReplacementTransform(step1, step2),
            run_time=0.5
        )
        
        # Highlight final relation
        box = SurroundingRectangle(step2, color=YELLOW, buff=0.2)
        self.play(
            ShowCreation(box),
            run_time=0.5
        )
        
        # Final highlight pulse on identity
        self.play(
            box.animate.set_color(RED).scale(1.1),
            run_time=0.5
        )