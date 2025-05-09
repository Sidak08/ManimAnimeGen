import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import base64
import io
import logging
import zipfile
import tempfile
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("manim_render.log")
    ]
)
logger = logging.getLogger("manim_renderer")

# Default Hugging Face Space URL for Manim rendering
DEFAULT_HF_SPACE_URL = "https://huggingface.co/spaces/YOUR_USERNAME/render-manim/api/predict"

class ManimHFRenderer:
    """Class to render Manim files using a Hugging Face Space."""
    
    def __init__(self, hf_space_url: str = None, api_key: Optional[str] = None):
        """
        Initialize the renderer with a Hugging Face Space URL.
        
        Args:
            hf_space_url (str): URL of the Hugging Face Space API endpoint
            api_key (Optional[str]): Hugging Face API key (if needed)
        """
        # First check environment variables, then fall back to default
        self.hf_space_url = hf_space_url or os.environ.get("HF_SPACE_URL", DEFAULT_HF_SPACE_URL)
        self.headers = {}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def prepare_files(self, manim_dir: Path) -> Dict[str, bytes]:
        """
        Prepare Manim files for submission to Hugging Face.
        
        Args:
            manim_dir (Path): Path to directory containing Manim files
            
        Returns:
            Dict[str, bytes]: Dictionary of filenames to file contents
        """
        logger.info(f"Preparing files from {manim_dir}")
        
        if not manim_dir.exists():
            raise FileNotFoundError(f"Directory {manim_dir} does not exist")
        
        files = {}
        
        # Add all Python files
        for py_file in manim_dir.glob("**/*.py"):
            relative_path = py_file.relative_to(manim_dir)
            with open(py_file, "rb") as f:
                files[str(relative_path)] = f.read()
        
        # Add any supporting files (images, data, etc.)
        extensions = [".png", ".jpg", ".jpeg", ".svg", ".csv", ".json", ".txt"]
        for ext in extensions:
            for support_file in manim_dir.glob(f"**/*{ext}"):
                relative_path = support_file.relative_to(manim_dir)
                with open(support_file, "rb") as f:
                    files[str(relative_path)] = f.read()
        
        logger.info(f"Prepared {len(files)} files")
        return files
    
    def create_zip_archive(self, files: Dict[str, bytes]) -> bytes:
        """
        Create a zip archive from files.
        
        Args:
            files (Dict[str, bytes]): Dictionary of filenames to file contents
            
        Returns:
            bytes: Zip archive as bytes
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename, content in files.items():
                zip_file.writestr(filename, content)
        
        zip_buffer.seek(0)
        return zip_buffer.read()
    
    def extract_zip(self, zip_data: bytes, output_dir: Path) -> List[Path]:
        """
        Extract a zip archive to the specified directory.
        
        Args:
            zip_data (bytes): Zip archive as bytes
            output_dir (Path): Directory to extract files to
            
        Returns:
            List[Path]: List of extracted file paths
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        extracted_files = []
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
            for file in zip_ref.namelist():
                zip_ref.extract(file, output_dir)
                extracted_files.append(output_dir / file)
        
        return extracted_files
    
    def render(
        self, 
        manim_dir: Path, 
        scene_name: str,
        quality: str = "medium_quality",
        output_dir: Optional[Path] = None,
        main_file: Optional[str] = None
    ) -> Path:
        """
        Render a Manim scene using Hugging Face.
        
        Args:
            manim_dir (Path): Path to directory containing Manim files
            scene_name (str): Name of the scene to render
            quality (str): Quality of the rendering (low_quality, medium_quality, high_quality)
            output_dir (Optional[Path]): Directory to save the output video (defaults to current dir)
            main_file (Optional[str]): Main Python file to run (defaults to the first .py file)
            
        Returns:
            Path: Path to the rendered video file
        """
        if output_dir is None:
            output_dir = Path.cwd() / "renders"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Prepare files for submission
        files = self.prepare_files(manim_dir)
        
        # If main_file is not specified, try to find it
        if main_file is None:
            py_files = [f for f in files.keys() if f.endswith(".py")]
            if not py_files:
                raise ValueError(f"No Python files found in {manim_dir}")
            main_file = py_files[0]
            logger.info(f"Using {main_file} as main file")
        
        # Create zip archive
        zip_data = self.create_zip_archive(files)
        encoded_zip = base64.b64encode(zip_data).decode("utf-8")
        
        # Prepare payload
        payload = {
            "data": [
                encoded_zip,  # Zipped project
                main_file,    # Main Python file
                scene_name,   # Scene name
                quality,      # Quality
            ]
        }
        
        # Submit to Hugging Face Space
        logger.info(f"Submitting render job for scene {scene_name}")
        try:
            # Check if the Space URL contains a placeholder
            if "YOUR_USERNAME" in self.hf_space_url:
                raise ValueError(
                    "Invalid Space URL. Please update your .env file with your own "
                    "Hugging Face Space URL. See DEPLOYMENT.md for instructions."
                )
            
            response = requests.post(
                self.hf_space_url,
                headers=self.headers,
                json=payload,
                timeout=600  # 10-minute timeout
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error submitting render job: {e}")
            if hasattr(e, "response") and e.response is not None:
                logger.error(f"Response: {e.response.text}")
                
                # Provide more helpful error message for common issues
                if hasattr(e, "response") and e.response is not None:
                    if e.response.status_code == 404:
                        logger.error(
                            "404 Error: The Space URL was not found. Please check that:\n"
                            "1. You've created your own Hugging Face Space (see DEPLOYMENT.md)\n"
                            "2. The Space URL in your .env file is correct\n"
                            "3. The Space is successfully deployed (check Space status on Hugging Face)"
                        )
                    elif e.response.status_code == 401 or e.response.status_code == 403:
                        logger.error(
                            "Authentication Error: Your API key may be invalid or missing.\n"
                            "Make sure you've set the correct HF_API_KEY in your .env file."
                        )
                    elif e.response.status_code == 504 or e.response.status_code == 408:
                        logger.error(
                            "Timeout Error: The rendering process took too long.\n"
                            "Try a simpler scene or use a lower quality setting."
                        )
            raise
        
        # Process response
        try:
            result = response.json()
            if "error" in result:
                raise RuntimeError(f"Error from Hugging Face: {result['error']}")
            
            # Extract data from response
            data = result.get("data", [])
            if not data or len(data) < 2:
                raise ValueError("Invalid response from Hugging Face")
            
            render_status = data[0]
            if render_status != "success":
                raise RuntimeError(f"Rendering failed: {render_status}")
            
            # Get the base64-encoded video data
            video_data_base64 = data[1]
            if not video_data_base64:
                raise ValueError("No video data received")
            
            # Decode video data
            video_data = base64.b64decode(video_data_base64)
            
            # Save video file
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            output_file = output_dir / f"{scene_name}_{timestamp}.mp4"
            with open(output_file, "wb") as f:
                f.write(video_data)
            
            logger.info(f"Saved rendered video to {output_file}")
            return output_file
        
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            logger.error(f"Error processing response: {e}")
            logger.error(f"Response text: {response.text[:500]}...")
            raise
    
    def render_batch(
        self, 
        manim_dir: Path, 
        scene_names: List[str],
        quality: str = "medium_quality",
        output_dir: Optional[Path] = None,
        main_file: Optional[str] = None
    ) -> List[Path]:
        """
        Render multiple Manim scenes.
        
        Args:
            manim_dir (Path): Path to directory containing Manim files
            scene_names (List[str]): Names of the scenes to render
            quality (str): Quality of the rendering
            output_dir (Optional[Path]): Directory to save the output videos
            main_file (Optional[str]): Main Python file to run
            
        Returns:
            List[Path]: Paths to the rendered video files
        """
        output_files = []
        for scene_name in tqdm(scene_names, desc="Rendering scenes"):
            try:
                output_file = self.render(
                    manim_dir=manim_dir,
                    scene_name=scene_name,
                    quality=quality,
                    output_dir=output_dir,
                    main_file=main_file
                )
                output_files.append(output_file)
            except Exception as e:
                logger.error(f"Error rendering scene {scene_name}: {e}")
                continue
        
        return output_files
    
    @staticmethod
    def detect_scenes(manim_dir: Path) -> List[str]:
        """
        Detect scenes in Manim Python files.
        
        Args:
            manim_dir (Path): Path to directory containing Manim files
            
        Returns:
            List[str]: List of detected scene names
        """
        import ast
        
        class SceneVisitor(ast.NodeVisitor):
            def __init__(self):
                self.scenes = []
            
            def visit_ClassDef(self, node):
                # Check if class inherits from Scene
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "Scene":
                        self.scenes.append(node.name)
                    elif isinstance(base, ast.Name) and "Scene" in base.id:
                        # For cases like ThreeDScene, etc.
                        self.scenes.append(node.name)
                
                self.generic_visit(node)
        
        scenes = []
        for py_file in manim_dir.glob("**/*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())
                
                visitor = SceneVisitor()
                visitor.visit(tree)
                scenes.extend(visitor.scenes)
            except Exception as e:
                logger.warning(f"Error parsing {py_file}: {e}")
        
        return scenes

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Render Manim videos using Hugging Face")
    parser.add_argument(
        "manim_dir", 
        help="Path to directory containing Manim files",
        type=Path
    )
    parser.add_argument(
        "--scene", 
        help="Scene name to render (if not provided, will detect and render all scenes)",
        type=str
    )
    parser.add_argument(
        "--quality", 
        help="Quality of rendering (low_quality, medium_quality, high_quality)",
        choices=["low_quality", "medium_quality", "high_quality"],
        default=os.environ.get("DEFAULT_QUALITY", "medium_quality")
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save rendered videos",
        type=Path,
        default=os.environ.get("OUTPUT_DIR", None)
    )
    parser.add_argument(
        "--main-file",
        help="Main Python file to run",
        type=str,
        default=None
    )
    parser.add_argument(
        "--hf-space-url",
        help="Hugging Face Space URL for rendering",
        type=str,
        default=None  # Will be loaded from env or set to default later
    )
    parser.add_argument(
        "--api-key",
        help="Hugging Face API key",
        type=str,
        default=None
    )
    
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Load environment variables if .env file exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv not installed. Environment variables may not be loaded.")
        pass
    
    # Check if Space URL is set
    hf_space_url = args.hf_space_url or os.environ.get("HF_SPACE_URL")
    if not hf_space_url or "YOUR_USERNAME" in hf_space_url:
        print("\033[93mWARNING: Using default Space URL. This may not work!\033[0m")
        print("Please set up your own Hugging Face Space and update HF_SPACE_URL in your .env file.")
        print("See DEPLOYMENT.md for detailed instructions on setting up your own Space.")
        
        # Ask for confirmation
        if not args.hf_space_url:  # Only ask if not explicitly provided as argument
            answer = input("Continue anyway? [y/N] ")
            if answer.lower() != 'y':
                print("Exiting. Please set up your Space and try again.")
                sys.exit(1)
    
    # Initialize renderer
    renderer = ManimHFRenderer(
        hf_space_url=hf_space_url,
        api_key=args.api_key or os.environ.get("HF_API_KEY")
    )
    
    if args.scene:
        # Render single scene
        output_file = renderer.render(
            manim_dir=args.manim_dir,
            scene_name=args.scene,
            quality=args.quality,
            output_dir=args.output_dir,
            main_file=args.main_file
        )
        print(f"Rendered video saved to: {output_file}")
    else:
        # Detect and render all scenes
        scenes = renderer.detect_scenes(args.manim_dir)
        if not scenes:
            print("No scenes detected")
            return
        
        print(f"Detected {len(scenes)} scenes: {', '.join(scenes)}")
        
        # Ask for confirmation
        answer = input(f"Render all {len(scenes)} scenes? [y/N] ")
        if answer.lower() != 'y':
            scenes_to_render = []
            while not scenes_to_render:
                scene_input = input("Enter scene names to render (comma-separated): ")
                scenes_to_render = [s.strip() for s in scene_input.split(",") if s.strip()]
                
                # Validate scenes
                invalid_scenes = [s for s in scenes_to_render if s not in scenes]
                if invalid_scenes:
                    print(f"Invalid scenes: {', '.join(invalid_scenes)}")
                    scenes_to_render = []
        else:
            scenes_to_render = scenes
        
        output_files = renderer.render_batch(
            manim_dir=args.manim_dir,
            scene_names=scenes_to_render,
            quality=args.quality,
            output_dir=args.output_dir,
            main_file=args.main_file
        )
        
        print(f"Rendered {len(output_files)} videos:")
        for output_file in output_files:
            print(f"- {output_file}")

if __name__ == "__main__":
    main()