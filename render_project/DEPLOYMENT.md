# Deployment Guide: Setting Up Your Manim Renderer on Hugging Face

This guide will walk you through setting up your own Hugging Face Space to render Manim animations.

## Prerequisites

1. A Hugging Face account (sign up at [huggingface.co](https://huggingface.co/join))
2. Basic familiarity with Git

## Step 1: Create a New Hugging Face Space

1. Log in to your Hugging Face account
2. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
3. Click on "Create new Space"
4. Fill in the Space details:
   - **Owner**: Your username or organization
   - **Space name**: `render-manim` (or any name you prefer)
   - **License**: MIT (or your preference)
   - **Space SDK**: Gradio
   - **Space hardware**: CPU (T4 GPU is unnecessary for Manim rendering)
   - **Python version**: 3.9+

## Step 2: Upload the Space Files

### Option 1: Using the Web Interface

1. Navigate to your newly created Space
2. Click on "Files and versions"
3. Upload the following files from `huggingface_space/` directory:
   - `app.py`
   - `requirements.txt`
   - `README.md`

### Option 2: Using Git

1. Clone your Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/render-manim
   ```
2. Copy the files from `huggingface_space/` to this directory
3. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Initial commit for Manim renderer Space"
   git push
   ```

## Step 3: Wait for Deployment

1. After uploading files, Hugging Face will automatically build and deploy your Space
2. This can take 5-10 minutes depending on server load
3. You can monitor the build process in the "Settings" tab under "Build logs"

## Step 4: Update Your Environment Configuration

1. Once your Space is deployed, copy the API endpoint URL:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/render-manim/api/predict
   ```
2. Update your `.env` file:
   ```
   HF_SPACE_URL=https://huggingface.co/spaces/YOUR_USERNAME/render-manim/api/predict
   ```

## Step 5: Test Your Space

1. Run the example script to test your Space:
   ```bash
   python example.py
   ```
   
## Troubleshooting

### Common Issues

1. **404 Error**: Make sure the Space URL is correctly formatted and your Space is fully deployed
2. **Timeout Error**: The rendering process may be taking too long, try with a simpler Manim scene
3. **Authentication Errors**: Ensure your API key is correctly set in the `.env` file

### Space Resource Limits

Be aware that Hugging Face Spaces have resource limitations:
- CPU Spaces: 2 vCPU, 16GB RAM
- Storage: 5GB
- Timeout: 10 minutes for API calls

For complex animations, consider upgrading to a paid plan or optimizing your Manim code.

### Updating Your Space

To update your Space with new changes:
1. Make your changes to the files
2. Upload them again using the web interface or Git
3. The Space will automatically rebuild with your changes

## Support

If you encounter any issues with the Space itself, check the Space logs in the Hugging Face interface under the "Settings" tab.