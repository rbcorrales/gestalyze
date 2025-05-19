import argparse
import os
import pickle
from pathlib import Path
import mediapipe as mp
import cv2
import numpy as np
from tqdm import tqdm

from config import (
    get_dataset_paths,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    MAX_NUM_HANDS,
    MODEL_COMPLEXITY
)

def extract_landmarks_from_image(image_path, mp_hands, mp_drawing):
    """Extract hand landmarks from a single image."""
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Warning: Could not read image {image_path}")
        return None

    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(image_rgb)

    if not results.multi_hand_landmarks:
        return None

    # Get the first hand's landmarks and convert to pickleable format
    hand_landmarks = results.multi_hand_landmarks[0]
    landmarks_list = []
    for landmark in hand_landmarks.landmark:
        landmarks_list.append({
            'x': landmark.x,
            'y': landmark.y,
            'z': landmark.z,
            'visibility': landmark.visibility
        })
    return landmarks_list

def extract_landmarks_from_directory(directory, mp_hands, mp_drawing):
    """Extract hand landmarks from all images in a directory."""
    landmarks = {}
    image_files = list(Path(directory).glob("**/*.jpg")) + list(Path(directory).glob("**/*.png"))
    
    for image_path in tqdm(image_files, desc=f"Processing {directory}"):
        hand_landmarks = extract_landmarks_from_image(image_path, mp_hands, mp_drawing)
        if hand_landmarks:
            # Use relative path as key
            rel_path = str(image_path.relative_to(directory))
            landmarks[rel_path] = hand_landmarks

    return landmarks

def main():
    parser = argparse.ArgumentParser(description="Extract hand landmarks from training and test datasets")
    parser.add_argument("--dataset-name", required=True, help="Name of the dataset directory in datasets/")
    args = parser.parse_args()

    # Get dataset paths
    paths = get_dataset_paths(args.dataset_name)
    train_dir = paths['raw']['train']
    test_dir = paths['raw']['test']
    train_output = paths['landmarks']['train']
    test_output = paths['landmarks']['test']

    # Initialize MediaPipe
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=MAX_NUM_HANDS,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        model_complexity=MODEL_COMPLEXITY
    )

    # Process training data
    print(f"\nProcessing training data from {train_dir}")
    train_landmarks = extract_landmarks_from_directory(train_dir, hands, mp_drawing)
    
    # Process test data
    print(f"\nProcessing test data from {test_dir}")
    test_landmarks = extract_landmarks_from_directory(test_dir, hands, mp_drawing)

    # Save landmarks
    os.makedirs(os.path.dirname(train_output), exist_ok=True)
    os.makedirs(os.path.dirname(test_output), exist_ok=True)
    
    with open(train_output, 'wb') as f:
        pickle.dump(train_landmarks, f)
    with open(test_output, 'wb') as f:
        pickle.dump(test_landmarks, f)

    print(f"\nSaved landmarks to:")
    print(f"Training: {train_output}")
    print(f"Test: {test_output}")

if __name__ == "__main__":
    main()
