import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from config import TRAIN_DATA_PATH, TEST_DATA_PATH, MODEL_PATH, RANDOM_STATE

def load_data(train_path, test_path):
    """Load training and test datasets."""
    with open(train_path, 'rb') as f:
        train_data = pickle.load(f)
    
    with open(test_path, 'rb') as f:
        test_data = pickle.load(f)
    
    return train_data, test_data

def train_and_evaluate():
    """Train and evaluate the ASL classifier."""
    # Load data
    print("Loading datasets...")
    train_data, test_data = load_data(TRAIN_DATA_PATH, TEST_DATA_PATH)
    
    # Prepare features and labels
    X_train, y_train = train_data['features'], train_data['labels']
    X_test, y_test = test_data['features'], test_data['labels']
    
    # Initialize and train the model
    print("\nTraining Random Forest Classifier...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=RANDOM_STATE
    )
    
    model.fit(X_train, y_train)
    
    # Make predictions
    print("\nEvaluating model...")
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")
    
    # Print detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    print(f"\nSaving model to {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)
    print("Model saved successfully!")

if __name__ == "__main__":
    train_and_evaluate()
