#!/bin/bash

# Check if output directory was provided
if [ $# -lt 1 ]; then
    echo "Usage: ./generate_manim_dataset.sh [output_dir]"
    echo "  output_dir: (Optional) Output directory for the final dataset (default: manim_dataset)"
    exit 1
fi

# Get command line arguments
SOURCE_DIR="../manim_trig.py"
VIDEO_DIR="../media/videos/manim_trig/1080p60/partial_movie_files/TrigIdentity"
OUTPUT_DIR="${1:-manim_dataset}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Starting Manim dataset generation pipeline..."
echo "---------------------------------------------"
echo "Source code directory: $SOURCE_DIR"
echo "Video directory: $VIDEO_DIR"
echo "Output directory: $OUTPUT_DIR"
echo "---------------------------------------------"

echo "Step 1: Analyzing Manim source code..."
python auto_labeler.py "$SOURCE_DIR" "$OUTPUT_DIR/code_analysis.json"
if [ $? -ne 0 ]; then
    echo "Error in Step 1: Source code analysis failed."
    exit 1
fi

echo "Step 2: Extracting frames from videos..."
python frame_extractor.py "$VIDEO_DIR" "$OUTPUT_DIR/code_analysis.json" "$OUTPUT_DIR/merged_dataset.json"
if [ $? -ne 0 ]; then
    echo "Error in Step 2: Frame extraction failed."
    exit 1
fi

echo "Step 3: Adding mathematics-specific labels..."
python math_labeler.py "$OUTPUT_DIR/merged_dataset.json" "$OUTPUT_DIR/math_dataset.json"
if [ $? -ne 0 ]; then
    echo "Error in Step 3: Math labeling failed."
    exit 1
fi

echo "Step 4: Creating machine learning dataset..."
python create_ml_dataset.py "$OUTPUT_DIR/math_dataset.json" "$OUTPUT_DIR/ml_dataset"
if [ $? -ne 0 ]; then
    echo "Error in Step 4: ML dataset creation failed."
    exit 1
fi

echo "---------------------------------------------"
echo "Dataset generation complete!"
echo "Find your dataset in $OUTPUT_DIR/ml_dataset"
echo "---------------------------------------------"