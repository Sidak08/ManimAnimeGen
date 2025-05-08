from manim import *

class SimpleTrig(Scene):
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
        point = 2 * np.array([np.cos(angle), np.sin(angle), 0])
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
        
        # Animation sequence
        
        # Step 1: Show title
        self.play(Write(title))
        
        # Step 2: Draw circle and axes
        self.play(Create(axes))
        self.play(Create(circle), FadeIn(origin))
        
        # Add Unit Circle label
        circle_label = Text("Unit Circle", font_size=36)
        circle_label.to_corner(UL)
        self.play(FadeIn(circle_label))
        
        # Step 3: Show angle and radius
        self.play(Create(angle_arc), Write(angle_label))
        self.play(Create(radius))
        
        # Step 4: Show point on circle
        self.play(FadeIn(dot))
        
        # Step 5: Show sin and cos components
        self.play(Create(x_line), Create(y_line))
        self.play(Write(sin_label), Write(cos_label))
        
        # Step 6: Show identity
        self.play(Write(identity))
        
        # Step 7: Highlight identity
        box = SurroundingRectangle(identity, color=YELLOW, buff=0.2)
        self.play(Create(box))
        
        # Final message
        final_text = Text("A fundamental identity in trigonometry", font_size=36)
        final_text.next_to(title, DOWN)
        self.play(Write(final_text))
        
        self.wait(2)