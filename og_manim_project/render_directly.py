import os
import subprocess
from pathlib import Path

# Determine paths
desktop_path = os.path.expanduser("~/Desktop")
output_file = os.path.join(desktop_path, "trig_identities.mp4")
scene_file = "videos/trig_simple.py"
scene_class = "TrigSimple"
images_dir = os.path.join(os.getcwd(), "videos", "images", scene_class)

# Ensure output directory exists
Path(images_dir).mkdir(parents=True, exist_ok=True)

print(f"Starting the rendering process for {scene_class}...")

# Run manimgl with -i flag to save the images directly
manimgl_cmd = ["manimgl", scene_file, scene_class, "-i"]
print(f"Running: {' '.join(manimgl_cmd)}")
subprocess.run(manimgl_cmd)

# Check if frames were generated
frame_files = list(Path(images_dir).glob("*.png"))
if not frame_files:
    print(f"No frames found in {images_dir}.")
    exit(1)

print(f"Found {len(frame_files)} frames")

# Sort frames by name
frame_files.sort()

# Use ffmpeg to convert frames to video
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
    print(f"Running: {' '.join(ffmpeg_cmd)}")
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
        "-vcodec", "h264",
        output_file
    ]
    try:
        print(f"Running: {' '.join(alt_cmd)}")
        subprocess.run(alt_cmd, check=True)
        print(f"Success with alternative method! Video saved to {output_file}")
    except subprocess.CalledProcessError:
        print("Failed to create video. Check if frames were generated correctly.")