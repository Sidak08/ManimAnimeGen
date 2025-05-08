import os
import json
import sys
import glob
import numpy as np
from PIL import Image
import h5py
from tqdm import tqdm

def create_ml_dataset(math_dataset_path, output_dir):
    import re  # Import for regex patterns
    """Create a machine learning dataset from the enhanced math dataset"""
    with open(math_dataset_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Define dataset structure
    ml_dataset = {
        'code_snippets': [],  # Source code snippets
        'animation_sequences': [],  # Animation sequences
        'math_expressions': [],  # Math expressions
        'domains': [],  # Mathematical domains
        'frame_paths': [],  # Paths to key frames
    }
    
    
    # Find all extracted frames
    all_frames = []
    frame_dirs = []
    scene_frame_matches = {}
    
    # First pass: collect all frame directories
    collected_frame_dirs = []
    search_dirs = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(math_dataset_path))), "media", "videos"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(math_dataset_path))), "videos"),
        "../media/videos",
        "../videos"
    ]
    
    for base_dir in search_dirs:
        if not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            if "frames_" in root and os.path.exists(root):
                collected_frame_dirs.append(root)
    
    print(f"Found {len(collected_frame_dirs)} frame directories")
    
    # Function to calculate matching score between scene and frame directory
    def calculate_scene_frame_match(scene_name, frame_dir):
        score = 0
        dir_name = os.path.basename(frame_dir)
        parent_dir = os.path.basename(os.path.dirname(frame_dir))
        
        # Exact match gets highest score
        if scene_name.lower() in dir_name.lower():
            score += 50
        
        # Parent directory matches scene name
        if scene_name.lower() in parent_dir.lower():
            score += 30
        
        # Check for scene name in the full path
        if scene_name.lower() in frame_dir.lower():
            score += 20
            
        # Check for partial matches in directory name
        scene_words = set(scene_name.replace("_", " ").lower().split())
        dir_words = set(dir_name.replace("_", " ").lower().split())
        parent_words = set(parent_dir.replace("_", " ").lower().split())
        
        matching_words_dir = scene_words.intersection(dir_words)
        matching_words_parent = scene_words.intersection(parent_words)
        
        score += len(matching_words_dir) * 5
        score += len(matching_words_parent) * 3
        
        return score
    
    # Score all frame directories for each scene
    for scene_data in dataset:
        scene_name = scene_data['scene_name']
        print(f"Looking for frames for scene: {scene_name}")
        scene_scores = []
        
        for frame_dir in collected_frame_dirs:
            score = calculate_scene_frame_match(scene_name, frame_dir)
            if score > 0:
                scene_scores.append((frame_dir, score))
        
        # Sort by score in descending order
        scene_scores.sort(key=lambda x: x[1], reverse=True)
        scene_frame_matches[scene_name] = scene_scores
        
        # Get best matches
        if scene_scores:
            best_dir, best_score = scene_scores[0]
            if best_score >= 10:
                print(f"Best match for '{scene_name}': {best_dir} (score: {best_score})")
            else:
                print(f"No good match found for '{scene_name}' (best score: {best_score})")
        else:
            print(f"No matches found for '{scene_name}'")
    
    # Second pass: process scenes with their matched frame directories
    for scene_data in dataset:
        scene_name = scene_data['scene_name']
        matched_dirs = scene_frame_matches.get(scene_name, [])
        found_frames = False
        
        for frame_dir, score in matched_dirs[:3]:  # Use top 3 matches
            if score < 10:  # Skip low-scoring matches
                continue
                    frame_files = glob.glob(os.path.join(frame_dir, "*.jpg"))
                    if frame_files:
                        frame_dirs.append(frame_dir)
                        print(f"Found {len(frame_files)} frames in {frame_dir}")
                        found_frames = True
                        
                        # Check if we can correlate frames with animation structure
                        # Sort frame files to ensure proper sequence
                        sorted_frames = sorted(frame_files)
                        
                        # Try to infer animation points from frame timestamps or filenames
                        timestamp_pattern = re.compile(r'_(\d+\.\d+)\.jpg$')
                        frame_timestamps = []
                        
                        for frame in sorted_frames:
                            match = timestamp_pattern.search(frame)
                            if match:
                                timestamp = float(match.group(1))
                                frame_timestamps.append((frame, timestamp))
                        
                        if frame_timestamps:
                            # Sort by timestamp
                            frame_timestamps.sort(key=lambda x: x[1])
                            sorted_frames = [f[0] for f in frame_timestamps]
                        
                        # Analyze frame transitions to find key points
                        # This is a simple approach - with more time we could use image analysis
                        key_frames = []
                        
                        if len(sorted_frames) <= 4:  # For very few frames, use all of them
                            key_frames = sorted_frames
                        else:
                            # Take frames at regular intervals, with higher density at beginning
                            step = max(1, len(sorted_frames) // min(20, len(scene_data.get('steps', []))))
                            key_frames = [sorted_frames[i] for i in range(0, len(sorted_frames), step)]
                            # Ensure first and last frames are included
                            if sorted_frames[0] not in key_frames:
                                key_frames.insert(0, sorted_frames[0])
                            if sorted_frames[-1] not in key_frames:
                                key_frames.append(sorted_frames[-1])
                        
                        # Distribute frames among steps
                        step_count = len(scene_data.get('steps', []))
                        if step_count > 0:
                            frames_per_step = len(sorted_frames) / step_count
                            
                            for step_idx in range(step_count):
                                start_idx = int(step_idx * frames_per_step)
                                end_idx = int((step_idx + 1) * frames_per_step)
                                
                                step_frames = sorted_frames[start_idx:end_idx]
                                if step_frames:
                                    if 'frames' not in scene_data['steps'][step_idx]:
                                        scene_data['steps'][step_idx]['frames'] = []
                                    scene_data['steps'][step_idx]['frames'].extend(step_frames)
                                    all_frames.extend(step_frames)
        
        if found_frames:
            print(f"Successfully assigned frames to {scene_name}")
    
    # Optional: prepare for image data storage
    image_data_path = os.path.join(output_dir, 'image_data.h5')
    with h5py.File(image_data_path, 'w') as h5f:
        # Create dataset for images - we'll resize all to a standard size
        img_dataset = h5f.create_dataset(
            'images', 
            shape=(0, 224, 224, 3),  # Initial shape with 0 images
            maxshape=(None, 224, 224, 3),  # Allows us to resize later
            dtype=np.uint8,
            chunks=(1, 224, 224, 3)  # Chunk size for efficient access
        )
        
        # Process scenes
        total_frames = 0
        scene_indices = []
        
        # First pass to count frames
        for scene_data in dataset:
            for step in scene_data.get('steps', []):
                frames = step.get('frames', [])
                if frames:
                    total_frames += len(frames)
                    
        if total_frames == 0:
            print("No frames found in steps, using all discovered frames")
            total_frames = len(all_frames)
        
        if total_frames > 0:
            # Resize the dataset
            img_dataset.resize((total_frames, 224, 224, 3))
            
            frame_idx = 0
            
            # If no frames in steps but we found frames in directories
            if len(all_frames) > 0 and not any(len(step.get('frames', [])) > 0 for scene in dataset for step in scene.get('steps', [])):
                print(f"Using {len(all_frames)} discovered frames")
                for frame_path in tqdm(sorted(all_frames), desc="Processing discovered frames"):
                    try:
                        img = Image.open(frame_path)
                        img = img.resize((224, 224))  # Standard size for ML models
                        img_array = np.array(img)
                        
                        # Handle grayscale images
                        if len(img_array.shape) == 2:
                            img_array = np.stack([img_array, img_array, img_array], axis=2)
                        elif img_array.shape[2] == 4:  # Handle RGBA
                            img_array = img_array[:, :, :3]
                        
                        # Store the image
                        if frame_idx < img_dataset.shape[0]:
                            img_dataset[frame_idx] = img_array
                            frame_idx += 1
                    except Exception as e:
                        print(f"Error processing image {frame_path}: {e}")
            
            # Second pass to process data
            for scene_data in tqdm(dataset, desc="Processing scenes"):
                # Add code snippet
                ml_dataset['code_snippets'].append(scene_data['source_code'])
                
                # Add animation sequence
                animation_seq = []
                for step in scene_data.get('steps', []):
                    if step['type'] == 'animation':
                        animation_seq.append(step['data'])
                ml_dataset['animation_sequences'].append(animation_seq)
                
                # Add math expressions and domain
                math_labels = scene_data.get('math_labels', {})
                ml_dataset['math_expressions'].append(math_labels.get('expressions', []))
                ml_dataset['domains'].append(math_labels.get('primary_domain', 'unknown'))
                
                # Process frames
                scene_frames = []
                for step in scene_data.get('steps', []):
                    frames = step.get('frames', [])
                    if frames:
                        # Take middle frame as key frame
                        middle_idx = len(frames) // 2
                        middle_frame_path = frames[middle_idx]
                        scene_frames.append(middle_frame_path)
                        
                        # Load and preprocess the image
                        try:
                            img = Image.open(middle_frame_path)
                            img = img.resize((224, 224))  # Standard size for ML models
                            img_array = np.array(img)
                            
                            # Handle grayscale images
                            if len(img_array.shape) == 2:
                                img_array = np.stack([img_array, img_array, img_array], axis=2)
                            elif img_array.shape[2] == 4:  # Handle RGBA
                                img_array = img_array[:, :, :3]
                            
                            # Store the image
                            if frame_idx < img_dataset.shape[0]:
                                img_dataset[frame_idx] = img_array
                                frame_idx += 1
                        except Exception as e:
                            print(f"Error processing image {middle_frame_path}: {e}")
                
                ml_dataset['frame_paths'].append(scene_frames)
                scene_indices.append(frame_idx)
            
            # Store scene indices for reference
            h5f.create_dataset('scene_indices', data=np.array(scene_indices))
        else:
            print("No frames found in dataset, creating metadata only")
    
    # Save metadata separately
    metadata_path = os.path.join(output_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(ml_dataset, f, indent=2)
    
    print(f"Machine learning dataset created at {output_dir}")
    print(f"Image data stored in {image_data_path}")
    print(f"Metadata stored in {metadata_path}")
    
    # Create splits for training, validation and testing
    create_data_splits(output_dir)

def create_data_splits(dataset_dir):
    """Create train, validation, and test splits for the dataset"""
    metadata_path = os.path.join(dataset_dir, 'metadata.json')
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Get total number of samples
    num_samples = len(metadata['code_snippets'])
    
    if num_samples == 0:
        print("No samples in dataset, skipping data splits")
        return
        
    # Create indices and shuffle
    indices = np.arange(num_samples)
    np.random.shuffle(indices)
    
    # Split ratios (70% train, 15% validation, 15% test)
    train_ratio = 0.7
    val_ratio = 0.15
    
    train_size = int(num_samples * train_ratio)
    val_size = int(num_samples * val_ratio)
    
    # Create splits
    train_indices = indices[:train_size].tolist()
    val_indices = indices[train_size:train_size + val_size].tolist()
    test_indices = indices[train_size + val_size:].tolist()
    
    # Save splits
    splits = {
        'train': train_indices,
        'validation': val_indices,
        'test': test_indices
    }
    
    splits_path = os.path.join(dataset_dir, 'data_splits.json')
    with open(splits_path, 'w', encoding='utf-8') as f:
        json.dump(splits, f, indent=2)
    
    print(f"Data splits created and saved to {splits_path}")
    print(f"Train: {len(train_indices)} samples")
    print(f"Validation: {len(val_indices)} samples")
    print(f"Test: {len(test_indices)} samples")

def main():
    """Create a machine learning dataset from the enhanced math dataset"""
    if len(sys.argv) < 2:
        print("Usage: python create_ml_dataset.py <math_dataset_path> [output_directory]")
        return
    
    math_dataset_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "manim_ml_dataset"
    
    create_ml_dataset(math_dataset_path, output_dir)

if __name__ == "__main__":
    main()