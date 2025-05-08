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
    
    # Create a dictionary to map scene names to video files
    # This is a heuristic and may need to be adjusted based on your naming conventions
    scene_to_video = {}
    for video_path in frames_data.keys():
        video_name = os.path.basename(video_path)
        
        # Extract scene name from video filename 
        # Assumes that video names contain scene class names
        for scene in code_dataset:
            scene_name = scene['scene_name']
            if scene_name.lower() in video_name.lower():
                scene_to_video[scene_name] = video_path
    
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

def main():
    """Process video files to extract frames and merge with code analysis"""
    if len(sys.argv) < 3:
        print("Usage: python frame_extractor.py <video_directory> <code_dataset_path> [output_path]")
        return
    
    video_dir = sys.argv[1]
    code_dataset_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "manim_merged_dataset.json"
    
    frames_data = {}
    
    if os.path.isdir(video_dir):
        # Process all video files in the directory
        for root, _, files in os.walk(video_dir):
            for file in files:
                if file.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    video_path = os.path.join(root, file)
                    
                    # Create output directory for frames
                    base_name = os.path.splitext(file)[0]
                    frames_dir = os.path.join(root, f"frames_{base_name}")
                    
                    print(f"Processing video: {video_path}")
                    frames_data[video_path] = extract_frames_from_video(video_path, frames_dir)
    
    elif os.path.isfile(video_dir) and video_dir.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # Process a single video file
        video_path = video_dir
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        frames_dir = os.path.join(os.path.dirname(video_path), f"frames_{base_name}")
        
        frames_data[video_path] = extract_frames_from_video(video_path, frames_dir)
    
    else:
        print(f"Invalid video path: {video_dir}")
        return
    
    # Merge the code analysis with the extracted frames
    merge_code_and_frames(code_dataset_path, frames_data, output_path)

if __name__ == "__main__":
    main()