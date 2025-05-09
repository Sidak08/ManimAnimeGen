# Manim Renderer with Hugging Face Integration

This tool provides an easy way to render Manim animations using Hugging Face Spaces without requiring a local Manim installation.

> **🆕 New User?** Start with [QUICKSTART.md](./QUICKSTART.md) for faster setup!

## Features

- Send Manim files to Hugging Face for rendering
- Automatically detect scenes in Python files
- Support for batch rendering multiple scenes
- Different quality options (low, medium, high)
- Local storage of rendered videos

## Installation

1. Clone this repository or download the scripts
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
```

4. Deploy your own Hugging Face Space:
   - Follow the detailed instructions in [DEPLOYMENT.md](./DEPLOYMENT.md)
   - Update the `.env` file with your Space URL
   
5. Test your Space connection:
```bash
python test_space.py
```

## Usage

### Basic Usage

To render a specific scene:

```bash
python render_manim_hf.py /path/to/manim/directory --scene SceneName
```

To detect and render all scenes:

```bash
python render_manim_hf.py /path/to/manim/directory
```

You can also use the provided example script:

```bash
python example.py /path/to/manim/directory --scene SceneName
```

### Command-line Options

```
usage: render_manim_hf.py [-h] [--scene SCENE] [--quality {low_quality,medium_quality,high_quality}]
                         [--output-dir OUTPUT_DIR] [--main-file MAIN_FILE]
                         [--hf-space-url HF_SPACE_URL] [--api-key API_KEY]
                         manim_dir

Render Manim videos using Hugging Face

positional arguments:
  manim_dir             Path to directory containing Manim files

options:
  -h, --help            show this help message and exit
  --scene SCENE         Scene name to render (if not provided, will detect and render all scenes)
  --quality {low_quality,medium_quality,high_quality}
                        Quality of rendering (low_quality, medium_quality, high_quality)
  --output-dir OUTPUT_DIR
                        Directory to save rendered videos
  --main-file MAIN_FILE
                        Main Python file to run
  --hf-space-url HF_SPACE_URL
                        Hugging Face Space URL for rendering
  --api-key API_KEY     Hugging Face API key
```

## Examples

### Render a specific scene with high quality

```bash
python render_manim_hf.py ./my_manim_project --scene TrigIdentity --quality high_quality --output-dir ./videos
```

### Detect and render all scenes in a project

```bash
python render_manim_hf.py ./my_manim_project --quality medium_quality
```

### Render from a specific Python file

```bash
python render_manim_hf.py ./my_manim_project --scene TrigIdentity --main-file trigonometry.py
```

### Using the shell script wrapper

```bash
./render.sh --scene TrigIdentity --quality high_quality ./my_manim_project
```

## Setting up Hugging Face 

This tool requires access to a working Hugging Face Space that can render Manim animations. 

### Creating your own Space (Recommended)

We've provided the code for a Hugging Face Space in the `huggingface_space` directory.

**Quick Setup:**
1. Create an account on [Hugging Face](https://huggingface.co/)
2. Create a new Space (Gradio app)
3. Upload the files from `huggingface_space` directory to your Space
4. Once deployed, update your `.env` file with your Space's URL

**Detailed instructions:**
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for step-by-step guide
- For quick testing, use [test_space.py](./test_space.py) to verify your setup

### Using an existing Space

If you have access to an existing Manim rendering Space:

1. Create a `.env` file in the same directory as the script
2. Set the Space URL: `HF_SPACE_URL=https://huggingface.co/spaces/username/space-name/api/predict`
3. If needed, add your API key: `HF_API_KEY=your_api_key_here`

## Supported Project Structure

Your Manim project structure can be as simple as:

```
my_manim_project/
├── main.py           # Main Python file with scene definitions
├── helper.py         # Optional additional modules
└── assets/           # Optional directory for images or other resources
    └── logo.png
```

The script will automatically package all necessary files and send them to Hugging Face for rendering.

## Troubleshooting

- Check the `manim_render.log` file for detailed logs if rendering fails
- Ensure your Manim code is compatible with the version used by the Hugging Face Space
- For large projects, consider splitting them into smaller pieces to avoid timeout issues
- If you get a 404 error, make sure the Hugging Face Space URL is correct and the Space is running
- Most errors with "Not Found" are due to incorrect Space URLs in the `.env` file

### Connectivity Issues

If you're experiencing connectivity problems with your Space:

1. Run the test script to verify your setup:
   ```bash
   python test_space.py
   ```
   
2. Check your Space status on the Hugging Face website
3. Verify your API key has proper permissions
4. Review the Space build logs for any deployment errors

See the [DEPLOYMENT.md](./DEPLOYMENT.md) guide for more troubleshooting tips.