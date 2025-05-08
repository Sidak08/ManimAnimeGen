#!/bin/bash

# Check command-line arguments
if [ $# -lt 1 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo "Usage: ./generate_manim_dataset.sh [SOURCE_DIR] [VIDEO_DIR] [output_dir]"
    echo "  SOURCE_DIR: Directory or file with Manim source code (default: ../manim_trig.py)"
    echo "  VIDEO_DIR: Directory with rendered videos (default: ../media/videos)"
    echo "  output_dir: Output directory for the final dataset (default: manim_dataset)"
    exit 1
fi

# Get command line arguments
SOURCE_DIR="${1:-../og_manim_project/manim_trig.py}"
VIDEO_DIR="${2:-../media/videos/manim_trig/1080p60/partial_movie_files/TrigIdentity}"
OUTPUT_DIR="${3:-manim_dataset}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Starting Manim dataset generation pipeline..."
echo "---------------------------------------------"
echo "Source code directory/file: $SOURCE_DIR"
echo "Video directory: $VIDEO_DIR"
echo "Output directory: $OUTPUT_DIR"
echo "---------------------------------------------"

echo "Step 1: Analyzing Manim source code..."
if [ -d "$SOURCE_DIR" ]; then
    echo "Processing directory of source files..."
    python auto_labeler.py "$SOURCE_DIR" "$OUTPUT_DIR/code_analysis.json"
else
    echo "Processing single source file..."
    python auto_labeler.py "$SOURCE_DIR" "$OUTPUT_DIR/code_analysis.json"
fi

if [ $? -ne 0 ]; then
    echo "Error in Step 1: Source code analysis failed."
    exit 1
fi

echo "Step 2: Extracting frames from videos..."
echo "This process may take time for large video directories..."
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

echo "Dataset summary:"
echo "- Source code analysis: $OUTPUT_DIR/code_analysis.json"
echo "- Merged data with frames: $OUTPUT_DIR/merged_dataset.json"
echo "- Math enriched data: $OUTPUT_DIR/math_dataset.json"
echo "- Machine learning dataset: $OUTPUT_DIR/ml_dataset/"
echo "  - Metadata: $OUTPUT_DIR/ml_dataset/metadata.json"
echo "  - Image data: $OUTPUT_DIR/ml_dataset/image_data.h5"
echo "  - Data splits: $OUTPUT_DIR/ml_dataset/data_splits.json"