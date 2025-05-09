from manimlib import *
import os

# Configuration - automatically save to desktop
DESKTOP_PATH = os.path.expanduser("~/Desktop")
OUTPUT_FILE = os.path.join(DESKTOP_PATH, "trig_identity.mp4")

class TrigIdentity(Scene):
    def construct(self):
        # Title
        title = Text("Trigonometric Identity", font_size=60)
        title.to_edge(UP, buff=0.5)
        
        # Unit circle setup
        circle = Circle(radius=2, color=WHITE)
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            axis_config={"include_tip": False}
        )
        origin = Dot(ORIGIN, color=WHITE)
        
        # Point at 45 degrees
        point = np.array([np.sqrt(2), np.sqrt(2), 0])
        dot = Dot(point, color=RED)
        
        # Lines
        x_line = Line(ORIGIN, [point[0], 0, 0], color=GREEN, stroke_width=5)
        y_line = Line([point[0], 0, 0], point, color=BLUE, stroke_width=5)
        radius_line = Line(ORIGIN, point, color=YELLOW, stroke_width=3)
        
        # Labels
        sin_label = Tex("\\sin(\\theta) = \\frac{\\sqrt{2}}{2}", font_size=36, color=BLUE)
        sin_label.next_to(y_line, RIGHT, buff=0.2)
        
        cos_label = Tex("\\cos(\\theta) = \\frac{\\sqrt{2}}{2}", font_size=36, color=GREEN)
        cos_label.next_to(x_line, DOWN, buff=0.2)
        
        # Angle
        angle_arc = Arc(radius=0.7, angle=PI/4, color=YELLOW)
        theta_label = Tex("\\theta = 45°", font_size=36, color=YELLOW)
        theta_label.move_to([0.5, 0.3, 0])
        
        # Pythagorean identity
        identity = Tex("\\sin^2\\theta + \\cos^2\\theta = 1", font_size=48)
        identity.to_edge(DOWN, buff=1.5)
        
        # Proof with values
        proof = Tex("\\left(\\frac{\\sqrt{2}}{2}\\right)^2 + \\left(\\frac{\\sqrt{2}}{2}\\right)^2 = \\frac{1}{2} + \\frac{1}{2} = 1", font_size=36)
        proof.next_to(identity, UP, buff=0.5)
        
        # Animation sequence
        
        # Intro
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        # Set up unit circle
        self.play(
            ShowCreation(axes),
            ShowCreation(circle),
            run_time=1
        )
        
        unit_circle_text = Text("Unit Circle", font_size=36)
        unit_circle_text.to_corner(UL)
        
        self.play(
            Write(unit_circle_text),
            ShowCreation(origin),
            run_time=1
        )
        
        # Point and angle
        self.play(
            ShowCreation(angle_arc),
            ShowCreation(radius_line),
            Write(theta_label),
            run_time=1
        )
        
        self.play(
            ShowCreation(dot),
            run_time=0.5
        )
        
        # Show sin and cos
        self.play(
            ShowCreation(x_line),
            ShowCreation(y_line),
            run_time=1
        )
        
        self.play(
            Write(sin_label),
            Write(cos_label),
            run_time=1
        )
        
        # Show identity
        self.play(
            Write(identity),
            run_time=1
        )
        
        # Show proof
        self.play(
            Write(proof),
            run_time=1.5
        )
        
        # Highlight
        box = SurroundingRectangle(identity, color=YELLOW, buff=0.2)
        self.play(
            ShowCreation(box),
            run_time=1
        )
        
        # Final
        final_text = Text("A fundamental identity in trigonometry", font_size=36)
        final_text.next_to(title, DOWN)
        self.play(
            Write(final_text),
            run_time=1
        )
        
        self.wait(1)

# Force non-interactive rendering
if __name__ == "__main__":
    from manimlib.config import get_configuration
    from manimlib.extract_scene import scene_classes_from_file
    
    config = get_configuration()
    # Override config to force write file
    config["write_to_movie"] = True
    config["output_file"] = OUTPUT_FILE
    config["preview"] = False
    config["quiet"] = True
    config["from_animation_number"] = 0
    config["upto_animation_number"] = float("inf")
    
    for SceneClass in scene_classes_from_file(__file__):
        scene = SceneClass(config)
        scene.render()
    
    print(f"Animation has been saved to: {OUTPUT_FILE}")