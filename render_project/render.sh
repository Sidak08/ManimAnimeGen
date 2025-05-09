#!/bin/bash
# Manim Renderer Helper Script

# Default values
SCENE=""
QUALITY="medium_quality"
OUTPUT_DIR="./renders"
MAIN_FILE=""
HF_API_KEY=""

# Display usage information
function show_help {
    echo "Manim Renderer with Hugging Face Integration"
    echo "--------------------------------------------"
    echo "Usage: ./render.sh [options] <manim_directory>"
    echo ""
    echo "Options:"
    echo "  -s, --scene <name>       Scene name to render"
    echo "  -q, --quality <quality>  Rendering quality (low_quality, medium_quality, high_quality)"
    echo "  -o, --output <dir>       Output directory for rendered videos"
    echo "  -m, --main <file>        Main Python file to run"
    echo "  -k, --key <api_key>      Hugging Face API key"
    echo "  -h, --help               Show this help message"
    echo ""
    echo "Example:"
    echo "  ./render.sh --scene TrigIdentity --quality high_quality ../og_manim_project"
    exit 0
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--scene)
            SCENE="$2"
            shift 2
            ;;
        -q|--quality)
            QUALITY="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -m|--main)
            MAIN_FILE="$2"
            shift 2
            ;;
        -k|--key)
            HF_API_KEY="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            ;;
        -*)
            echo "Unknown option: $1"
            show_help
            ;;
        *)
            MANIM_DIR="$1"
            shift
            ;;
    esac
done

# Check if manim directory was provided
if [ -z "$MANIM_DIR" ]; then
    echo "Error: Manim directory not specified."
    show_help
fi

# Check if manim directory exists
if [ ! -d "$MANIM_DIR" ]; then
    echo "Error: Directory '$MANIM_DIR' not found."
    exit 1
fi

# Check if HF_API_KEY is set in environment or .env file
if [ -z "$HF_API_KEY" ] && [ -f .env ]; then
    source .env
fi

# Construct the command
CMD="python3 render_manim_hf.py '$MANIM_DIR'"

if [ -n "$SCENE" ]; then
    CMD="$CMD --scene '$SCENE'"
fi

if [ -n "$QUALITY" ]; then
    CMD="$CMD --quality '$QUALITY'"
fi

if [ -n "$OUTPUT_DIR" ]; then
    CMD="$CMD --output-dir '$OUTPUT_DIR'"
fi

if [ -n "$MAIN_FILE" ]; then
    CMD="$CMD --main-file '$MAIN_FILE'"
fi

if [ -n "$HF_API_KEY" ]; then
    CMD="$CMD --api-key '$HF_API_KEY'"
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run the command
echo "Running: $CMD"
eval $CMD