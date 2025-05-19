import numpy as np

def preprocess_landmarks(landmarks, model_type='custom'):
    """
    Preprocess hand landmarks for model input.
    
    Args:
        landmarks: List of hand landmarks (21 points with x, y coordinates)
        model_type: Type of model ('custom' or 'online')
        
    Returns:
        np.ndarray: Flattened and normalized feature vector
    """
    # Extract features directly from landmarks
    features = []
    for landmark in landmarks:
        # Use only x, y coordinates (42 features)
        features.extend([landmark.x, landmark.y])
    
    # Convert to numpy array
    features = np.array(features)
    
    # Reshape to match the format used during training
    features = features.reshape(1, -1)
    
    return features

def extract_landmarks_from_mediapipe(hand_landmarks):
    """
    Extract landmarks from MediaPipe hand landmarks object.
    
    Args:
        hand_landmarks: MediaPipe hand landmarks object
        
    Returns:
        list: List of landmarks with x, y coordinates
    """
    return hand_landmarks.landmark
