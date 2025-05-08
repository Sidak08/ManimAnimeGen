import os
import subprocess
import shutil
from pathlib import Path

# Configuration
SCENE_FILE = "videos/trig_identities_30sec.py"
SCENE_CLASS = "TrigIdentities30Seconds"
OUTPUT_FOLDER = os.path.expanduser("~/Desktop")
OUTPUT_FILENAME = "trig_identities_30sec.mp4"

# Create directories for rendering
images_dir = Path("videos/images")
images_dir.mkdir(exist_ok=True, parents=True)

scene_images_dir = images_dir / SCENE_CLASS
if scene_images_dir.exists():
    shutil.rmtree(scene_images_dir)

# Step 1: Render the animation frames
print(f"Rendering {SCENE_CLASS}...")
render_command = f"manimgl {SCENE_FILE} {SCENE_CLASS} -w"
subprocess.run(render_command, shell=True)

# Step 2: Check if rendering was successful
if not scene_images_dir.exists() or not any(scene_images_dir.iterdir()):
    print("Rendering failed or no frames were generated.")
    exit(1)

# Step 3: Use ffmpeg to combine frames into a video
output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)
print(f"Creating video at {output_path}...")

# Build ffmpeg command
ffmpeg_cmd = [
    "ffmpeg",
    "-y",  # Overwrite output file if it exists
    "-framerate", "30",  # Frame rate
    "-i", f"{scene_images_dir}/%05d.png",  # Input pattern
    "-c:v", "libx264",  # Video codec
    "-pix_fmt", "yuv420p",  # Pixel format
    "-crf", "18",  # Quality (lower is better)
    output_path
]

# Run ffmpeg command
subprocess.run(ffmpeg_cmd)

# Check if video was created
if os.path.exists(output_path):
    print(f"Successfully created video at {output_path}")
else:
    print("Failed to create video.")