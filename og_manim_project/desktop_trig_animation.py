import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch
import os
from pathlib import Path

# Save location
desktop_path = os.path.expanduser("~/Desktop")
output_file = os.path.join(desktop_path, "trig_identity.mp4")

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.grid(alpha=0.3)
ax.set_title('Trigonometric Identity: $\\sin^2\\theta + \\cos^2\\theta = 1$', fontsize=16)

# Unit circle
unit_circle = Circle((0, 0), 1, fill=False, edgecolor='gray', linestyle='-', linewidth=2)
ax.add_patch(unit_circle)

# Axis labels
ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
ax.text(1.1, 0.1, 'x', fontsize=12)
ax.text(0.1, 1.1, 'y', fontsize=12)

# Point on circle (45 degrees)
theta = np.pi/4
x = np.cos(theta)
y = np.sin(theta)

# Elements to animate
point, = ax.plot([x], [y], 'ro', markersize=10)
radius, = ax.plot([0, x], [0, y], 'y-', linewidth=2)
x_line, = ax.plot([0, x], [0, 0], 'g-', linewidth=3)
y_line, = ax.plot([x, x], [0, y], 'b-', linewidth=3)

# Correct Arc constructor for matplotlib
angle_arc = Arc((0, 0), 0.4, 0.4, theta1=0, theta2=theta*180/np.pi, color='y', linewidth=2)
ax.add_patch(angle_arc)

# Text for labels
ax.text(-0.2, -0.2, 'O', fontsize=14)
ax.text(x/2, -0.2, '$\\cos\\theta$', fontsize=14, color='green')
ax.text(x+0.1, y/2, '$\\sin\\theta$', fontsize=14, color='blue')
ax.text(0.25, 0.15, '$\\theta$', fontsize=14, color='orange')

# Add proof text
proof_text = ax.text(0, -1.5, '', fontsize=16, ha='center')
identity_box = Rectangle((0, 0), 0, 0, fill=False, edgecolor='y', linewidth=2)
ax.add_patch(identity_box)  # Add empty box initially

# Animation frames
def update(frame):
    if frame < 10:
        # Frame 0-9: Setup
        proof_text.set_text("")
        identity_box.set_bounds(0, 0, 0, 0)
        return point, radius, x_line, y_line, proof_text, identity_box
    
    elif frame < 20:
        # Frame 10-19: Show cos²θ + sin²θ
        eq = "$\\cos^2\\theta + \\sin^2\\theta = ?$"
        proof_text.set_text(eq)
        identity_box.set_bounds(0, 0, 0, 0)
        return point, radius, x_line, y_line, proof_text, identity_box
    
    elif frame < 30:
        # Frame 20-29: Show values
        eq = "$\\left(\\frac{\\sqrt{2}}{2}\\right)^2 + \\left(\\frac{\\sqrt{2}}{2}\\right)^2 = \\frac{1}{2} + \\frac{1}{2} = 1$"
        proof_text.set_text(eq)
        identity_box.set_bounds(0, 0, 0, 0)
        return point, radius, x_line, y_line, proof_text, identity_box
    
    elif frame < 40:
        # Frame 30-39: Final identity
        eq = "$\\sin^2\\theta + \\cos^2\\theta = 1$"
        proof_text.set_text(eq)
        
        # Create box around the text
        bbox = proof_text.get_window_extent()
        display_bbox = ax.transData.inverted().transform(bbox)
        x0, y0 = display_bbox[0]
        x1, y1 = display_bbox[1]
        width = x1 - x0
        height = y1 - y0
        identity_box.set_bounds(x0-0.3, y0-0.1, width+0.6, height+0.2)
        
        return point, radius, x_line, y_line, proof_text, identity_box
    
    # Frame 40+: Final state
    return point, radius, x_line, y_line, proof_text, identity_box

# Create animation
ani = animation.FuncAnimation(
    fig, update, frames=50, interval=100, blit=True
)

# Add title at the bottom
plt.figtext(0.5, 0.01, "Understanding the Pythagorean Identity", fontsize=14, ha='center')

# Save animation
print(f"Generating animation and saving to {output_file}...")
ani.save(output_file, writer='ffmpeg', fps=10, dpi=150)
print(f"Animation saved to {output_file}")

plt.close()