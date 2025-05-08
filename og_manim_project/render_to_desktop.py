import os
import subprocess
import time
from pathlib import Path

# Determine paths
desktop_path = os.path.expanduser("~/Desktop")
output_file = os.path.join(desktop_path, "trig_identities.mp4")
images_dir = os.path.join(os.getcwd(), "videos", "images", "TrigSimple")
Path(images_dir).mkdir(parents=True, exist_ok=True)

print("Starting the rendering process...")

# Step 1: Generate frames using manimgl
# Note: This opens an interactive window. Once the animation plays,
# press 'd' to save frames, then close the window when finished
manimgl_cmd = ["manimgl", "videos/trig_simple.py", "TrigSimple"]
print("Running ManimGL... When the animation plays, press 'd' to save frames")
print("Then close the window when animation finishes.")
subprocess.run(manimgl_cmd)

# Wait for frames to be saved
input("Press Enter after you've closed the ManimGL window and saved frames (pressed 'd')...")

# Check if frames were generated
if not os.path.exists(images_dir) or len(os.listdir(images_dir)) == 0:
    print(f"No frames found in {images_dir}. Make sure you pressed 'd' to save frames.")
    exit(1)

print(f"Found {len(os.listdir(images_dir))} frames")

# Step 2: Use ffmpeg to convert frames to video
print(f"Creating video on desktop: {output_file}")
ffmpeg_cmd = [
    "ffmpeg", 
    "-y",  # Overwrite output file if it exists
    "-framerate", "30", 
    "-pattern_type", "glob",
    "-i", f"{images_dir}/*.png", 
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p", 
    output_file
]

try:
    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Success! Video saved to {output_file}")
except subprocess.CalledProcessError:
    print("Error: Failed to create video with ffmpeg.")
    # Try an alternative ffmpeg command
    print("Trying alternative ffmpeg command...")
    alt_cmd = [
        "ffmpeg",
        "-y",
        "-framerate", "30",
        "-i", f"{images_dir}/%05d.png",
        "-vcodec", "png",
        output_file
    ]
    try:
        subprocess.run(alt_cmd, check=True)
        print(f"Success with alternative method! Video saved to {output_file}")
    except subprocess.CalledProcessError:
        print("Failed to create video. Please install ffmpeg or check if frames were generated correctly.")