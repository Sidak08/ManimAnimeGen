#!/usr/bin/env python3
import os
import sys
import argparse
import requests
import base64
import json
import time
from pathlib import Path
from dotenv import load_dotenv

def parse_args():
    parser = argparse.ArgumentParser(description="Test Hugging Face Space connectivity for Manim rendering")
    parser.add_argument("--space-url", help="Hugging Face Space URL to test")
    parser.add_argument("--api-key", help="Hugging Face API key")
    return parser.parse_args()

def create_minimal_manim_project():
    """Create a minimal Manim project for testing."""
    temp_dir = Path("./temp_test_project")
    temp_dir.mkdir(exist_ok=True)
    
    # Create a simple Manim file
    test_file = temp_dir / "test_scene.py"
    with open(test_file, "w") as f:
        f.write("""
from manim import *

class TestScene(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        self.play(Create(circle))
        self.wait(1)
        square = Square()
        square.set_fill(RED, opacity=0.5)
        self.play(Transform(circle, square))
        self.wait(1)
        text = Text("Hello, Manim!")
        self.play(Write(text))
        self.wait(1)
""")
    
    print(f"Created test Manim project at {temp_dir.absolute()}")
    return temp_dir

def create_zip_archive(directory):
    """Create a ZIP archive of the directory."""
    import zipfile
    import io
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in directory.glob("**/*"):
            if file_path.is_file():
                arcname = file_path.relative_to(directory)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    return zip_buffer.read()

def test_space_connection(space_url, api_key=None):
    """Test if the Space is properly set up and can render a simple Manim scene."""
    print(f"Testing connection to Space: {space_url}")
    
    # Create a minimal test project
    project_dir = create_minimal_manim_project()
    
    # Create a ZIP archive of the project
    zip_data = create_zip_archive(project_dir)
    encoded_zip = base64.b64encode(zip_data).decode("utf-8")
    
    # Prepare headers
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # Prepare payload
    payload = {
        "data": [
            encoded_zip,       # Zipped project
            "test_scene.py",   # Main Python file
            "TestScene",       # Scene name
            "low_quality",     # Quality (use low quality for faster test)
        ]
    }
    
    try:
        # Make a simple request to check if the Space is accessible
        print("Sending initial request to check Space accessibility...")
        response = requests.head(space_url, timeout=10)
        if response.status_code >= 400:
            print(f"Error: Space returned HTTP {response.status_code}")
            print("Please check your Space URL and ensure the Space is deployed and running.")
            return False
        
        # Submit the render job
        print("Submitting test render job...")
        start_time = time.time()
        response = requests.post(
            space_url,
            headers=headers,
            json=payload,
            timeout=300  # 5-minute timeout
        )
        
        # Check response
        if response.status_code == 200:
            try:
                result = response.json()
                if "data" in result and len(result["data"]) >= 1:
                    render_status = result["data"][0]
                    if render_status == "success":
                        print(f"✅ Success! Space responded with a successful render in {time.time() - start_time:.2f} seconds.")
                        return True
                    else:
                        print(f"❌ Space returned an error: {render_status}")
                        if len(result["data"]) > 1:
                            print(f"Error message: {result['data'][1]}")
                else:
                    print("❌ Space returned an unexpected response format.")
            except json.JSONDecodeError:
                print("❌ Space returned non-JSON response.")
                print(f"Response: {response.text[:500]}...")
        else:
            print(f"❌ Space returned HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}...")
        
        return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error: Could not connect to the Space.")
        print("Please check your internet connection and Space URL.")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout error: The Space took too long to respond.")
        print("This could indicate the Space is still building or is overloaded.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False
    finally:
        # Clean up
        import shutil
        shutil.rmtree(project_dir, ignore_errors=True)

def main():
    # Parse command-line arguments
    args = parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get Space URL from args, env, or default
    space_url = args.space_url or os.environ.get("HF_SPACE_URL")
    if not space_url:
        print("Error: No Space URL provided.")
        print("Please provide a Space URL with --space-url or set HF_SPACE_URL in your .env file.")
        sys.exit(1)
    
    # Get API key from args or env
    api_key = args.api_key or os.environ.get("HF_API_KEY")
    
    # Test the connection
    if test_space_connection(space_url, api_key):
        print("\nYour Hugging Face Space is correctly set up and working!")
        print("You can now use the Manim renderer with this Space.")
        sys.exit(0)
    else:
        print("\nConnection test failed. Please review the error messages above.")
        print("You can find detailed deployment instructions in DEPLOYMENT.md")
        sys.exit(1)

if __name__ == "__main__":
    main()