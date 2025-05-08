from manim import *
import os

# Set output file directly to desktop
desktop_path = os.path.expanduser("~/Desktop")

class TrigIdentity(Scene):
    def construct(self):
        # Title
        title = Text("Trigonometric Identity", font_size=60)
        title.to_edge(UP, buff=0.5)
        
        # Create unit circle
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
        
        # Animation sequence
        
        # Step 1: Show title
        self.play(Write(title))
        self.wait(0.5)
        
        # Step 2: Draw circle and axes
        self.play(
            Create(axes),
            Create(circle),
            Create(origin)
        )
        
        circle_label = Text("Unit Circle", font_size=36)
        circle_label.to_corner(UL)
        self.play(Write(circle_label))
        self.wait(0.5)
        
        # Step 3: Show angle and radius
        self.play(
            Create(angle_arc),
            Write(angle_label),
            Create(radius)
        )
        self.wait(0.5)
        
        # Step 4: Show point on circle
        self.play(FadeIn(dot))
        self.wait(0.5)
        
        # Step 5: Show sin and cos components
        self.play(
            Create(x_line),
            Create(y_line)
        )
        self.wait(0.5)
        
        self.play(
            Write(sin_label),
            Write(cos_label)
        )
        self.wait(0.5)
        
        # Step 6: Show identity
        self.play(Write(identity))
        self.wait(0.5)
        
        # Step 7: Show proof
        self.play(Write(proof))
        self.wait(0.5)
        
        # Step 8: Highlight identity
        box = SurroundingRectangle(identity, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(0.5)
        
        # Step 9: Final message
        final_text = Text("A fundamental identity in trigonometry", font_size=36)
        final_text.next_to(title, DOWN)
        self.play(Write(final_text))
        self.wait(1)

# Run the scene with -o flag to save to desktop
if __name__ == "__main__":
    command = f"manim -pqh {__file__} TrigIdentity -o"
    os.system(command)