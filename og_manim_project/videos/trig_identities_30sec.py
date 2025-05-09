from manimlib import *

class TrigIdentities30Seconds(Scene):
    def construct(self):
        # Title sequence
        title = Text("Essential Trigonometric Identities", font_size=60)
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("in 30 seconds", font_size=36, color=YELLOW)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Unit circle
        circle = Circle(radius=2, color=WHITE)
        origin = Dot(ORIGIN, color=WHITE)
        
        # Add coordinates and axis
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            axis_config={"include_tip": False}
        )
        
        # Prepare dynamic point on circle
        def get_point(angle):
            return np.array([2*np.cos(angle), 2*np.sin(angle), 0])
        
        # Starting angle
        angle = ValueTracker(PI/6)  # 30 degrees
        
        # Dynamic elements
        dot = Dot(color=RED)
        dot.add_updater(lambda d: d.move_to(get_point(angle.get_value())))
        
        # Lines for sin and cos (dynamic)
        x_line = Line(color=GREEN, stroke_width=5)
        x_line.add_updater(lambda l: l.put_start_and_end_on(
            [0, 0, 0], [get_point(angle.get_value())[0], 0, 0]
        ))
        
        y_line = Line(color=BLUE, stroke_width=5)
        y_line.add_updater(lambda l: l.put_start_and_end_on(
            [get_point(angle.get_value())[0], 0, 0], get_point(angle.get_value())
        ))
        
        radius_line = Line(color=YELLOW, stroke_width=3)
        radius_line.add_updater(lambda l: l.put_start_and_end_on(
            [0, 0, 0], get_point(angle.get_value())
        ))
        
        # Labels with updaters
        cos_label = Tex("\\cos\\theta", font_size=36, color=GREEN)
        cos_label.add_updater(lambda l: l.next_to(x_line, DOWN, buff=0.1))
        
        sin_label = Tex("\\sin\\theta", font_size=36, color=BLUE)
        sin_label.add_updater(lambda l: l.next_to(y_line, RIGHT, buff=0.1))
        
        # Angle visualization
        angle_arc = Arc(radius=0.7, color=YELLOW)
        angle_arc.add_updater(lambda a: a.become(
            Arc(radius=0.7, angle=angle.get_value(), color=YELLOW)
        ))
        
        theta_label = Tex("\\theta", font_size=42, color=YELLOW)
        theta_label.add_updater(lambda t: t.move_to(
            [0.4*np.cos(angle.get_value()/2), 0.4*np.sin(angle.get_value()/2), 0]
        ))
        
        # Main identities
        identity1 = Tex("\\sin^2\\theta + \\cos^2\\theta = 1", font_size=48)
        identity1.to_edge(DOWN, buff=1.5)
        identity1_box = SurroundingRectangle(identity1, color=YELLOW, buff=0.2)
        identity1_group = VGroup(identity1, identity1_box)
        
        identity2 = Tex("\\sin(\\theta + \\pi/2) = \\cos\\theta", font_size=48)
        identity2.to_edge(DOWN, buff=1.5)
        identity2_box = SurroundingRectangle(identity2, color=YELLOW, buff=0.2)
        identity2_group = VGroup(identity2, identity2_box)
        
        identity3 = Tex("\\cos(\\theta + \\pi) = -\\cos\\theta", font_size=48)
        identity3.to_edge(DOWN, buff=1.5)
        identity3_box = SurroundingRectangle(identity3, color=YELLOW, buff=0.2)
        identity3_group = VGroup(identity3, identity3_box)
        
        formula_note = Text("These formulas work in radians!", font_size=24, color=RED)
        formula_note.next_to(identity1, DOWN, buff=0.3)
        
        # Animation sequence (30 seconds total)
        
        # Intro (5 seconds)
        self.play(Write(title), run_time=1.5)
        self.play(Write(subtitle), run_time=0.5)
        self.wait(0.5)
        
        # Set up unit circle (5 seconds)
        self.play(
            FadeOut(subtitle),
            ShowCreation(axes),
            ShowCreation(circle),
            ShowCreation(origin),
            run_time=2
        )
        
        unit_circle_text = Text("Unit Circle (r = 1)", font_size=36)
        unit_circle_text.to_corner(UL)
        
        self.play(
            Write(unit_circle_text),
            run_time=1
        )
        
        self.play(
            ShowCreation(angle_arc),
            Write(theta_label),
            ShowCreation(radius_line),
            run_time=1
        )
        
        # Show point on circle and components (5 seconds)
        self.play(
            ShowCreation(dot),
            ShowCreation(x_line),
            ShowCreation(y_line),
            run_time=1.5
        )
        
        self.play(
            Write(sin_label),
            Write(cos_label),
            run_time=1
        )
        
        # First identity (5 seconds)
        self.play(
            Write(identity1),
            run_time=1
        )
        
        self.play(
            ShowCreation(identity1_box),
            Write(formula_note),
            run_time=1
        )
        
        # Animation of the point moving - demonstrate identity (5 seconds)
        self.play(
            angle.animate.set_value(PI/2),  # 90 degrees
            run_time=2
        )
        
        # Second identity (5 seconds)
        self.play(
            FadeOut(identity1_group),
            FadeOut(formula_note),
            Write(identity2),
            run_time=1.5
        )
        
        self.play(
            angle.animate.set_value(PI),  # 180 degrees
            run_time=1.5
        )
        
        self.play(
            ShowCreation(identity2_box),
            run_time=0.5
        )
        
        # Third identity (5 seconds)
        self.play(
            FadeOut(identity2_group),
            Write(identity3),
            angle.animate.set_value(3*PI/2),  # 270 degrees
            run_time=1.5
        )
        
        self.play(
            ShowCreation(identity3_box),
            run_time=0.5
        )
        
        self.play(
            angle.animate.set_value(2*PI),  # 360 degrees
            run_time=1
        )
        
        # Final summary (2-3 seconds)
        final_text = Text("Understanding these identities is key to trigonometry!", font_size=36, color=YELLOW)
        final_text.to_edge(UP)
        
        self.play(
            FadeOut(unit_circle_text),
            FadeIn(final_text),
            run_time=1
        )
        
        self.wait(0.5)