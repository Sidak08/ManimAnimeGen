# Quickstart Guide: Manim Render with Hugging Face

This guide will help you quickly set up and use the Manim rendering service with Hugging Face.

## 1. Initial Setup (One-time)

### Clone the Repository
```bash
git clone https://github.com/your-username/manim-renderer
cd manim-renderer
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Up Your Own Hugging Face Space
1. **Create a Hugging Face account** if you don't have one at [huggingface.co](https://huggingface.co/join)
2. **Create a new Space**:
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Use "Gradio" as the SDK
   - Choose CPU hardware (T4 GPU not needed)

3. **Upload the Space files**:
   - Upload files from `huggingface_space/` directory to your Space
   - Wait for the Space to build (5-10 minutes)

### Configure Your Environment
1. **Set up your .env file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file**:
   - Add your Hugging Face API key from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Update the `HF_SPACE_URL` with your Space URL:
     ```
     HF_SPACE_URL=https://huggingface.co/spaces/YOUR_USERNAME/render-manim/api/predict
     ```

## 2. Basic Usage

### Render a Single Scene
```bash
python render_manim_hf.py /path/to/manim/project --scene SceneName
```

### Using the Example Script
```bash
python example.py --scene TrigIdentity
```

### Using the Shell Script (Unix/Mac)
```bash
./render.sh --scene ExampleScene --quality medium_quality /path/to/manim/project
```

## 3. Options and Customization

### Quality Options
- `--quality low_quality` - Faster rendering, lower resolution
- `--quality medium_quality` - Balanced (default)
- `--quality high_quality` - High resolution, slower rendering

### Output Directory
```bash
python render_manim_hf.py /path/to/manim/project --scene SceneName --output-dir ./my_videos
```

### Specify Main File
If your scene is in a specific Python file:
```bash
python render_manim_hf.py /path/to/manim/project --scene SceneName --main-file my_file.py
```

## 4. Finding Scenes in a Project

To list all available scenes in a Manim project:
```bash
python render_manim_hf.py /path/to/manim/project
```
When prompted, enter 'n' to avoid rendering all scenes, and the tool will list the available scenes.

## 5. Troubleshooting

### 404 Error
- Verify your Space URL is correct
- Check that your Space is successfully deployed
- See deployment logs on Hugging Face for errors

### Authentication Issues
- Make sure your API key is correctly set in the .env file
- Verify the API key is valid and has appropriate permissions

### Render Failures
- Check the `manim_render.log` file for detailed error messages
- Ensure your Manim code works with the latest Manim Community Edition

## Next Steps

For more detailed instructions on deployment and advanced usage, see:
- `DEPLOYMENT.md` - Full deployment guide for your Hugging Face Space
- `README.md` - Complete documentation of all features

For help with Manim itself, visit the [Manim Community Documentation](https://docs.manim.community/).