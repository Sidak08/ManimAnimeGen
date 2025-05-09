#!/usr/bin/env python3
from pathlib import Path
import os
import argparse
import sys
from dotenv import load_dotenv
from render_manim_hf import ManimHFRenderer

# Load environment variables from .env file if present
load_dotenv()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Example of using the Manim HF Renderer")
    parser.add_argument(
        "--scene", 
        help="Scene name to render",
        type=str,
        default="TrigIdentity"
    )
    parser.add_argument(
        "--quality", 
        help="Quality of rendering",
        choices=["low_quality", "medium_quality", "high_quality"],
        default="medium_quality"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the example."""
    args = parse_args()
    
    # Get API key from environment variable
    api_key = os.environ.get("HF_API_KEY")
    
    # Path to the example Manim project
    # This points to the project in the og_manim_project directory
    default_manim_dir = Path(__file__).parent.parent / "og_manim_project"
    
    # Check if a command-line argument was provided
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        manim_dir = Path(sys.argv[1])
    else:
        manim_dir = default_manim_dir
    
    if not manim_dir.exists():
        print(f"Example project directory not found: {manim_dir}")
        print("Please provide the path to a valid Manim project.")
        return
    
    print(f"Using Manim project directory: {manim_dir}")
    
    # Initialize the renderer
    # Get Space URL from environment variable
    hf_space_url = os.environ.get("HF_SPACE_URL")
    renderer = ManimHFRenderer(hf_space_url=hf_space_url, api_key=api_key)
    
    # Detect available scenes
    detected_scenes = renderer.detect_scenes(manim_dir)
    print(f"Detected scenes: {', '.join(detected_scenes)}")
    
    # Check if the requested scene exists
    scene_to_render = args.scene
    if detected_scenes and scene_to_render not in detected_scenes:
        print(f"Warning: Scene '{scene_to_render}' not found in the detected scenes.")
        print(f"Available scenes: {', '.join(detected_scenes)}")
        choice = input("Continue anyway? (y/n): ")
        if choice.lower() != 'y':
            return
    
    # Create output directory
    output_dir = Path(os.environ.get("OUTPUT_DIR", Path(__file__).parent / "renders"))
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"Rendering scene '{scene_to_render}' with {args.quality} quality...")
    
    # Render the scene
    try:
        output_file = renderer.render(
            manim_dir=manim_dir,
            scene_name=scene_to_render,
            quality=args.quality,
            output_dir=output_dir,
            main_file="manim_trig.py"  # Specify the main file for this example
        )
        
        print(f"Rendering successful!")
        print(f"Output video saved to: {output_file}")
        
        # Print the full path to the output file
        print(f"Full path: {output_file.absolute()}")
        
        # On some systems, we can automatically open the video
        try:
            if os.name == 'posix':  # Linux or macOS
                os.system(f"open '{output_file}'")
            elif os.name == 'nt':  # Windows
                os.system(f'start "" "{output_file}"')
        except Exception as e:
            print(f"Could not open video automatically: {e}")
            
    except Exception as e:
        print(f"Error rendering scene: {e}")

if __name__ == "__main__":
    main()