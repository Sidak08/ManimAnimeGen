#!/bin/bash

# Check command-line arguments
if [ $# -lt 1 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    echo "Usage: ./process_code_only.sh [SOURCE_DIR] [output_dir]"
    echo "  SOURCE_DIR: Directory or file with Manim source code (default: ../og_manim_project/manim_trig.py)"
    echo "  output_dir: Output directory for the dataset (default: code_dataset)"
    exit 1
fi

# Get command line arguments
SOURCE_DIR="${1:-../og_manim_project/manim_trig.py}"
OUTPUT_DIR="${2:-code_dataset}"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Starting Manim code analysis pipeline..."
echo "---------------------------------------------"
echo "Source code directory/file: $SOURCE_DIR"
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

echo "Step 2: Adding mathematics-specific labels..."
# Create a minimal merged dataset with just code data
cp "$OUTPUT_DIR/code_analysis.json" "$OUTPUT_DIR/merged_dataset.json"

python math_labeler.py "$OUTPUT_DIR/merged_dataset.json" "$OUTPUT_DIR/math_dataset.json"
if [ $? -ne 0 ]; then
    echo "Error in Step 2: Math labeling failed."
    exit 1
fi

echo "Step 3: Creating code-only dataset..."
python -c "
import json
import os
import sys

# Load the math dataset
with open('$OUTPUT_DIR/math_dataset.json', 'r') as f:
    dataset = json.load(f)

# Extract just code and math information
code_dataset = []
for scene in dataset:
    code_dataset.append({
        'scene_name': scene['scene_name'],
        'source_code': scene['source_code'],
        'objects': scene.get('objects', {}),
        'animations': scene.get('animations', []),
        'steps': scene.get('steps', []),
        'math_labels': scene.get('math_labels', {})
    })

# Create an ML-ready structure
ml_dataset = {
    'code_snippets': [scene['source_code'] for scene in code_dataset],
    'animation_sequences': [scene.get('animations', []) for scene in code_dataset],
    'math_expressions': [scene.get('math_labels', {}).get('expressions', []) for scene in code_dataset],
    'domains': [scene.get('math_labels', {}).get('primary_domain', 'unknown') for scene in code_dataset],
    'concepts': [scene.get('math_labels', {}).get('concepts', []) for scene in code_dataset]
}

# Save the final dataset
os.makedirs('$OUTPUT_DIR/ml_dataset', exist_ok=True)
with open('$OUTPUT_DIR/ml_dataset/metadata.json', 'w') as f:
    json.dump(ml_dataset, f, indent=2)

print(f'Processed {len(code_dataset)} scenes')
"

if [ $? -ne 0 ]; then
    echo "Error in Step 3: Dataset creation failed."
    exit 1
fi

echo "---------------------------------------------"
echo "Code analysis complete!"
echo "Find your dataset in $OUTPUT_DIR/ml_dataset"
echo "---------------------------------------------"

echo "Dataset summary:"
echo "- Source code analysis: $OUTPUT_DIR/code_analysis.json"
echo "- Math enriched data: $OUTPUT_DIR/math_dataset.json" 
echo "- Machine learning dataset: $OUTPUT_DIR/ml_dataset/metadata.json"