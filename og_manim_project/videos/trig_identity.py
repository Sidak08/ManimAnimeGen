from manimlib import *

class TrigIdentity(Scene):
    def construct(self):
        # Title and main identity
        title = Text("Fundamental Trigonometric Identity", font_size=42)
        title.to_edge(UP, buff=0.5)
        
        identity = Tex("\\sin^2\\theta + \\cos^2\\theta = 1", font_size=60)
        identity.next_to(title, DOWN, buff=0.5)
        
        # Unit circle for visualization
        circle = Circle(radius=2, color=WHITE)
        origin = Dot(ORIGIN, color=WHITE)
        
        # Initial angle 
        angle = 30 * DEGREES
        
        # Create angle
        angle_arc = Arc(radius=0.5, angle=angle, color=YELLOW)
        angle_label = Tex("\\theta", font_size=36, color=YELLOW)
        angle_label.next_to(angle_arc, RIGHT, buff=0.1)
        
        # Point on circle
        point = circle.point_at_angle(angle)
        dot = Dot(point, color=RED)
        
        # Create lines for sin and cos
        x_line = Line(ORIGIN, [point[0], 0, 0], color=GREEN)
        y_line = Line([point[0], 0, 0], point, color=BLUE)
        
        # Labels for sin and cos
        cos_label = Tex("\\cos\\theta", font_size=30, color=GREEN)
        cos_label.next_to(x_line, DOWN, buff=0.1)
        
        sin_label = Tex("\\sin\\theta", font_size=30, color=BLUE)
        sin_label.next_to(y_line, RIGHT, buff=0.1)
        
        # Visual proof - squares
        cos_square = Square(side_length=abs(point[0]))
        cos_square.move_to([point[0]/2, -abs(point[0])/2, 0])
        cos_square.set_color(GREEN)
        cos_square.set_fill(GREEN, opacity=0.3)
        
        sin_square = Square(side_length=abs(point[1]))
        sin_square.move_to([point[0] + abs(point[1])/2, point[1]/2, 0])
        sin_square.set_color(BLUE)
        sin_square.set_fill(BLUE, opacity=0.3)
        
        # Equation for the visual proof
        vis_eq = Tex("\\sin^2\\theta + \\cos^2\\theta = 1", font_size=48)
        vis_eq.to_edge(DOWN, buff=1)
        
        # Animation sequence (10 seconds total)
        
        # Introduce the identity (3 seconds)
        self.play(
            Write(title),
            run_time=1
        )
        self.play(
            Write(identity),
            run_time=1
        )
        self.wait(0.5)
        
        # Set up unit circle (2 seconds)
        self.play(
            ShowCreation(circle),
            ShowCreation(origin),
            run_time=1
        )
        
        circle_text = Text("Unit Circle (radius = 1)", font_size=24)
        circle_text.to_corner(UL)
        
        self.play(
            Write(circle_text),
            ShowCreation(angle_arc),
            Write(angle_label),
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
        
        # Show visual proof with squares (2 seconds)
        self.play(
            ShowCreation(cos_square),
            ShowCreation(sin_square),
            run_time=1
        )
        
        sum_text = Text("Area of squares = Area of unit circle", font_size=24)
        sum_text.next_to(vis_eq, UP, buff=0.5)
        
        self.play(
            Write(sum_text),
            Write(vis_eq),
            run_time=1
        )
        
        # Final pulse highlight on the identity
        frame = SurroundingRectangle(vis_eq, color=YELLOW)
        self.play(
            ShowCreation(frame),
            run_time=0.5
        )