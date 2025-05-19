import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from config import get_dataset_paths, RANDOM_STATE, TEST_SIZE

class CustomTrainer:
    def __init__(self, dataset_name, model_path):
        self.dataset_name = dataset_name
        self.model_path = model_path
        self.paths = get_dataset_paths(dataset_name)
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=RANDOM_STATE
        )

    def preprocess_features(self, landmarks):
        """Convert landmarks to feature vectors."""
        features = []
        for landmark in landmarks:
            # Use only x, y coordinates (42 features)
            features.extend([landmark['x'], landmark['y']])
        return np.array(features)

    def load_data(self):
        """Load and preprocess the dataset."""
        # Load landmarks
        with open(self.paths['landmarks']['train'], 'rb') as f:
            train_landmarks = pickle.load(f)
        with open(self.paths['landmarks']['test'], 'rb') as f:
            test_landmarks = pickle.load(f)

        # Extract features and labels
        X_train = []
        y_train = []
        X_test = []
        y_test = []

        # Process training data
        for image_path, landmarks in train_landmarks.items():
            if landmarks is not None:
                features = self.preprocess_features(landmarks)
                label = os.path.basename(os.path.dirname(image_path))
                X_train.append(features)
                y_train.append(label)

        # Process test data
        for image_path, landmarks in test_landmarks.items():
            if landmarks is not None:
                features = self.preprocess_features(landmarks)
                label = os.path.basename(os.path.dirname(image_path))
                X_test.append(features)
                y_test.append(label)

        # Convert to numpy arrays
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        X_test = np.array(X_test)
        y_test = np.array(y_test)

        # Scale features
        X_train = self.scaler.fit_transform(X_train)
        X_test = self.scaler.transform(X_test)

        return X_train, X_test, y_train, y_test

    def plot_confusion_matrix(self, y_true, y_pred, title):
        """Plot and save confusion matrix."""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(15, 15))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(title)
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # Save the plot
        os.makedirs('plots', exist_ok=True)
        plt.savefig(f'plots/{title.lower().replace(" ", "_")}.png')
        plt.close()

    def train(self):
        """Train the model."""
        print("Loading and preprocessing data...")
        X_train, X_test, y_train, y_test = self.load_data()

        print("Training model...")
        self.model.fit(X_train, y_train)

        # Evaluate the model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        print(f"Training accuracy: {train_score:.4f}")
        print(f"Test accuracy: {test_score:.4f}")

        # Print classification report
        y_pred = self.model.predict(X_test)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        # Plot confusion matrix
        self.plot_confusion_matrix(y_test, y_pred, "Custom Model Confusion Matrix")

        # Save the model and scaler
        model_dir = os.path.dirname(self.model_path)
        os.makedirs(model_dir, exist_ok=True)
        
        # Save model and scaler together
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, self.model_path)

        return self.model, self.scaler
