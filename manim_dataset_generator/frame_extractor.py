import os
import json
import sys
import cv2
import numpy as np
from PIL import Image
from datetime import datetime

def extract_frames_from_video(video_path, output_dir, fps_fraction=1):
    """
    Extract frames from a video file
    
    Parameters:
    - video_path: Path to the video file
    - output_dir: Directory to save frames
    - fps_fraction: Extract 1/fps_fraction of all frames
    
    Returns:
    - List of extracted frame paths with timestamps
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the video
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error opening video file {video_path}")
        return []
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    
    print(f"Video: {video_path}")
    print(f"FPS: {fps}")
    print(f"Frame count: {frame_count}")
    print(f"Duration: {duration:.2f} seconds")
    
    # Calculate the frame interval
    frame_interval = int(fps / fps_fraction)
    if frame_interval < 1:
        frame_interval = 1
    
    frames_data = []
    frame_idx = 0
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
            
        if frame_idx % frame_interval == 0:
            # Convert from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Save the frame
            timestamp = frame_idx / fps
            frame_path = os.path.join(output_dir, f"frame_{frame_idx:06d}_{timestamp:.3f}.jpg")
            
            # Save with PIL for better quality
            Image.fromarray(frame_rgb).save(frame_path)
            
            frames_data.append({
                'frame_index': frame_idx,
                'timestamp': timestamp,
                'path': frame_path
            })
            
            if frame_idx % 100 == 0:
                print(f"Extracted frame {frame_idx}/{frame_count} ({frame_idx/frame_count*100:.1f}%)")
        
        frame_idx += 1
    
    video.release()
    return frames_data

def calculate_similarity_score(scene_name, video_path):
    """
    Calculate a similarity score between a scene name and a video path
    Higher score means better match
    
    Parameters:
    - scene_name: Name of the scene class
    - video_path: Path to video file
    
    Returns:
    - Similarity score (integer)
    """
    video_name = os.path.basename(video_path)
    video_dir = os.path.dirname(video_path)
    score = 0
    
    # Exact match in filename gets highest score
    if scene_name == os.path.splitext(video_name)[0]:
        score += 100
    # Scene name contained in filename
    elif scene_name.lower() in video_name.lower():
        score += 50
    # Words from scene name in filename
    else:
        scene_words = scene_name.replace("_", " ").split()
        for word in scene_words:
            if len(word) > 2 and word.lower() in video_name.lower():
                score += 10
    
    # Check parent directories for scene name
    path_parts = video_dir.split(os.sep)
    for i, part in enumerate(path_parts):
        if scene_name.lower() == part.lower():
            score += 30
        elif scene_name.lower() in part.lower():
            score += 15
            
    # Check for timestamp-like patterns that might indicate a match
    # Videos are often named with timestamps when generated automatically
    if "partial_movie_files" in video_path and scene_name in video_path:
        score += 40
        
    return score

def merge_code_and_frames(code_dataset_path, frames_data, output_path):
    """
    Merge code analysis with extracted frames
    
    Parameters:
    - code_dataset_path: Path to the JSON file with code analysis
    - frames_data: Dictionary mapping video files to frame data
    - output_path: Path to save the merged dataset
    """
    # Load the code dataset
    with open(code_dataset_path, 'r', encoding='utf-8') as f:
        code_dataset = json.load(f)
    
    # Create a dictionary to map scene names to video files with advanced matching
    scene_to_video = {}
    scene_video_scores = {}  # Tracks similarity scores
    
    # First calculate similarity scores for all scenes and videos
    for scene in code_dataset:
        scene_name = scene['scene_name']
        scene_video_scores[scene_name] = []
        
        for video_path in frames_data.keys():
            score = calculate_similarity_score(scene_name, video_path)
            if score > 0:  # Only consider non-zero scores
                scene_video_scores[scene_name].append((video_path, score))
    
    # Sort by score and assign best matching videos to scenes
    for scene_name, scores in scene_video_scores.items():
        if scores:
            # Sort by score in descending order
            scores.sort(key=lambda x: x[1], reverse=True)
            best_video, best_score = scores[0]
            
            # Only assign if score is above a minimum threshold
            if best_score >= 10:
                scene_to_video[scene_name] = best_video
                print(f"Matched scene '{scene_name}' to video {os.path.basename(best_video)} (score: {best_score})")
            else:
                print(f"No good match found for scene '{scene_name}' (best score: {best_score})")
    
    merged_dataset = []
    
    for scene in code_dataset:
        scene_name = scene['scene_name']
        scene_data = {
            'scene_name': scene_name,
            'source_code': scene['source_code'],
            'objects': scene['objects'],
            'animations': scene['animations'],
            'steps': scene['steps'],
            'frames': []
        }
        
        # If we found a matching video for this scene
        if scene_name in scene_to_video:
            video_path = scene_to_video[scene_name]
            video_frames = frames_data[video_path]
            
            # Assign frames to animation steps
            # This is a simple heuristic dividing frames evenly among animation steps
            step_count = len(scene['steps'])
            if step_count > 0 and len(video_frames) > 0:
                frames_per_step = len(video_frames) / step_count
                
                for step_idx, step in enumerate(scene['steps']):
                    start_frame = int(step_idx * frames_per_step)
                    end_frame = int((step_idx + 1) * frames_per_step)
                    
                    step_frames = video_frames[start_frame:end_frame]
                    if step_idx < len(scene_data['steps']):
                        scene_data['steps'][step_idx]['frames'] = [
                            frame['path'] for frame in step_frames
                        ]
        
        merged_dataset.append(scene_data)
    
    # Save the merged dataset
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_dataset, f, indent=2)
    
    print(f"Merged dataset saved to {output_path} with {len(merged_dataset)} scenes")

def get_unique_id_from_name(name):
    """
    Extract a potential unique ID from a filename
    Looks for patterns like number_number_number or hash-like strings
    
    Parameters:
    - name: Filename or string to analyze
    
    Returns:
    - Extracted ID or None
    """
    import re
    
    # Look for patterns like number_number_number (common in manim outputs)
    pattern1 = re.compile(r'(\d+_\d+_\d+)')
    match = pattern1.search(name)
    if match:
        return match.group(1)
        
    # Look for hash-like strings (32+ hex chars)
    pattern2 = re.compile(r'([0-9a-f]{32,})', re.IGNORECASE)
    match = pattern2.search(name)
    if match:
        return match.group(1)
    
    return None

def main():
    """Process video files to extract frames and merge with code analysis"""
    if len(sys.argv) < 3:
        print("Usage: python frame_extractor.py <video_directory> <code_dataset_path> [output_path]")
        return
    
    video_dir = sys.argv[1]
    code_dataset_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "manim_merged_dataset.json"
    
    frames_data = {}
    video_metadata = {}  # Store additional metadata about videos
    
    if os.path.isdir(video_dir):
        # Group videos by common patterns to help with matching
        video_groups = {}
        
        # First pass to collect video paths and organize by potential scene
        for root, _, files in os.walk(video_dir):
            for file in files:
                if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    video_path = os.path.join(root, file)
                    
                    # Try to extract scene name from directory structure
                    path_parts = root.split(os.sep)
                    potential_scene_name = None
                    
                    # Look for "scene name" directory pattern
                    for part in reversed(path_parts):
                        if not part.startswith("_") and not part.isdigit() and part not in ["videos", "media", "partial_movie_files"]:
                            potential_scene_name = part
                            break
                    
                    # Store metadata
                    unique_id = get_unique_id_from_name(file)
                    video_metadata[video_path] = {
                        'filename': file,
                        'potential_scene': potential_scene_name,
                        'unique_id': unique_id
                    }
                    
                    # Group by potential scene
                    if potential_scene_name:
                        if potential_scene_name not in video_groups:
                            video_groups[potential_scene_name] = []
                        video_groups[potential_scene_name].append(video_path)
        
        # Process videos by group
        for group_name, group_videos in video_groups.items():
            print(f"Processing video group: {group_name} ({len(group_videos)} videos)")
            for video_path in group_videos:
                base_name = os.path.splitext(os.path.basename(video_path))[0]
                frames_dir = os.path.join(os.path.dirname(video_path), f"frames_{base_name}")
                
                print(f"Processing video: {video_path}")
                frames_data[video_path] = extract_frames_from_video(video_path, frames_dir)
        
        # Process any ungrouped videos
        ungrouped = [v for v in video_metadata.keys() if video_metadata[v]['potential_scene'] is None]
        for video_path in ungrouped:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            frames_dir = os.path.join(os.path.dirname(video_path), f"frames_{base_name}")
            
            print(f"Processing ungrouped video: {video_path}")
            frames_data[video_path] = extract_frames_from_video(video_path, frames_dir)
    
    elif os.path.isfile(video_dir) and video_dir.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # Process a single video file
        video_path = video_dir
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        frames_dir = os.path.join(os.path.dirname(video_path), f"frames_{base_name}")
        
        unique_id = get_unique_id_from_name(base_name)
        video_metadata[video_path] = {
            'filename': os.path.basename(video_path),
            'potential_scene': None,
            'unique_id': unique_id
        }
        
        frames_data[video_path] = extract_frames_from_video(video_path, frames_dir)
    
    else:
        print(f"Invalid video path: {video_dir}")
        return
    
    # Merge the code analysis with the extracted frames
    merge_code_and_frames(code_dataset_path, frames_data, output_path)

if __name__ == "__main__":
    main()