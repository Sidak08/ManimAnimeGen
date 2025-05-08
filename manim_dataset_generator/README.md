# Manim Dataset Generator

A tool for automatically generating labeled datasets from 3Blue1Brown (3b1b) Manim code and videos for AI training.

## Overview

This toolset analyzes Manim Python code used for mathematical animations (like those created by 3Blue1Brown) and extracts structured data about:

- Scene content and structure
- Mathematical objects and their properties
- Animation sequences
- Mathematical expressions and domains
- Visual frames from rendered videos

The result is a labeled dataset suitable for machine learning projects like:
- AI-assisted animation generation
- Automatic mathematical visualization
- Code generation from mathematical concepts

## Prerequisites

Before using this tool, ensure you have:

1. Python 3.7 or higher
2. The following Python packages:
   ```
   pip install numpy opencv-python pillow h5py tqdm
   ```
3. Manim source code files (.py)
4. Rendered Manim videos (.mp4)

## Usage

### Basic Usage

```bash
# Make script executable (if needed)
chmod +x generate_manim_dataset.sh

# Run with default settings
./generate_manim_dataset.sh

# Run with custom paths
./generate_manim_dataset.sh /path/to/source/code /path/to/videos output_directory
```

### Full Pipeline

The generator performs the following steps:

1. **Code Analysis**: Extracts scene structure, objects, and animation steps
2. **Frame Extraction**: Gets frames from videos and links them to animation steps
3. **Math Labeling**: Identifies mathematical concepts and domains
4. **ML Dataset Creation**: Creates structured dataset with train/val/test splits

### Advanced Usage

For large-scale processing:

```bash
# Process an entire directory of Manim source files
./generate_manim_dataset.sh /path/to/source/directory /path/to/videos output_directory

# Process a specific source file with a directory of videos
./generate_manim_dataset.sh /path/to/source.py /path/to/videos output_directory
```

## Output Structure

The generator creates the following structure:

```
output_directory/
├── code_analysis.json      # Raw code analysis results
├── merged_dataset.json     # Code + frames data
├── math_dataset.json       # Code + frames + math domain data
└── ml_dataset/
    ├── image_data.h5       # Frame images in HDF5 format
    ├── metadata.json       # Structured metadata
    └── data_splits.json    # Train/validation/test splits
```

## Advanced Name Matching

This version includes advanced matching between code and video files:

- Scene-to-video matching using similarity scoring
- Directory and filename pattern analysis
- Hierarchical matching based on path structure
- Frame distribution based on animation step analysis

## How it Works

### 1. auto_labeler.py

Extracts scene structures from Manim code using Python's ast module to find all scene classes, objects, animations, and mathematical expressions.

### 2. frame_extractor.py

Processes video files, extracts frames, and associates them with the appropriate scene classes using advanced matching techniques.

### 3. math_labeler.py

Analyzes mathematical expressions in the code to categorize content by mathematical domain and identify key concepts.

### 4. create_ml_dataset.py

Creates a structured ML-ready dataset with properly formatted input-output pairs and train/validation/test splits.

## Example Data Point

A typical data point in the final dataset includes:

- Code snippet for a mathematical animation
- Sequence of animation steps
- Mathematical expressions and their domain
- Rendered frames showing the visual output

## Customization

You can modify the scripts to:
- Change the frame extraction rate
- Adjust the matching algorithms
- Customize the mathematical domain categories
- Change how frames are distributed among animation steps

## Troubleshooting

- **No frames found**: Check if your video path is correct and contains rendered Manim videos
- **Poor matching**: Try adjusting the similarity scoring in frame_extractor.py
- **Memory issues**: For large datasets, consider batch processing by running on subsets of files

## License

This project is available under the MIT License.