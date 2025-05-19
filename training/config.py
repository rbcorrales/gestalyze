import os

# Base dataset directory
DATASETS_DIR = "datasets"

def get_dataset_paths(dataset_name):
    """Get paths for a specific dataset."""
    dataset_dir = os.path.join(DATASETS_DIR, dataset_name)
    return {
        'raw': {
            'train': os.path.join(dataset_dir, "Train"),
            'test': os.path.join(dataset_dir, "Test")
        },
        'landmarks': {
            'train': os.path.join(dataset_dir, "landmarks_train.pkl"),
            'test': os.path.join(dataset_dir, "landmarks_test.pkl")
        }
    }

# Model parameters
RANDOM_STATE = 42
TEST_SIZE = 0.2

# MediaPipe parameters for landmark extraction
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1
MODEL_COMPLEXITY = 1

# Default dataset for online training
DEFAULT_DATASET = "Marxulia/asl_sign_languages_alphabets_v03"
