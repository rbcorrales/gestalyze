from datasets import load_dataset
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from training.base_trainer import BaseTrainer
import cv2
import mediapipe as mp
from tqdm import tqdm
import random
import joblib
import os
import seaborn as sns
import matplotlib.pyplot as plt

class OnlineTrainer(BaseTrainer):
    def __init__(self, model_path, dataset_name="Marxulia/asl_sign_languages_alphabets_v03"):
        super().__init__("online_asl", model_path)
        self.dataset_name = dataset_name
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=True,
            max_num_hands=1,
            min_detection_confidence=0.7,
            model_complexity=1
        )

    def load_data(self):
        """Load and preprocess the online ASL dataset."""
        print(f"Loading dataset from {self.dataset_name}...")
        dataset = load_dataset(self.dataset_name)
        
        features_list = []
        labels_list = []
        
        print("Processing training data...")
        for item in tqdm(dataset['train']):
            # Convert image to numpy array
            image = np.array(item['image'])
            
            # Process with MediaPipe
            results = self.hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            if results.multi_hand_landmarks:
                # Get the first hand's landmarks
                landmarks = results.multi_hand_landmarks[0]
                
                # Extract and preprocess features
                features = self.preprocess_features(landmarks)
                features_list.append(features)
                labels_list.append(item['label'])
                
                # Apply data augmentation
                augmented_features = self.augment_features(features)
                if augmented_features is not None:
                    features_list.append(augmented_features)
                    labels_list.append(item['label'])
        
        # Convert to numpy arrays
        X = np.array(features_list)
        y = np.array(labels_list)
        
        # Apply standardization
        X = self.scaler.fit_transform(X)
        
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        return X_train, y_train, X_test, y_test

    def preprocess_features(self, landmarks):
        """Preprocess hand landmarks for model input."""
        features = []
        for landmark in landmarks.landmark:
            # Use only x, y coordinates (42 features)
            features.extend([landmark.x, landmark.y])
        
        # Convert to numpy array
        features = np.array(features)
        
        return features

    def augment_features(self, features):
        """Apply data augmentation to features."""
        # Skip augmentation for some samples to maintain original data
        if np.random.random() < 0.3:
            return None
            
        # Reshape features to match the structure
        n_landmarks = 21
        n_coords = 2  # Only x, y coordinates
        
        # Reshape to (n_landmarks, n_coords)
        features_reshaped = features.reshape(n_landmarks, n_coords)
        
        # Apply random noise
        noise_level = 0.02
        features_reshaped += np.random.normal(0, noise_level, features_reshaped.shape)
        
        # Apply random rotation (simplified)
        if np.random.random() < 0.5:
            # Rotate around origin (simplified)
            angle = np.random.uniform(-0.1, 0.1)
            cos_angle = np.cos(angle)
            sin_angle = np.sin(angle)
            
            for i in range(n_landmarks):
                x, y = features_reshaped[i, 0], features_reshaped[i, 1]
                features_reshaped[i, 0] = x * cos_angle - y * sin_angle
                features_reshaped[i, 1] = x * sin_angle + y * cos_angle
        
        # Flatten back to 1D
        augmented_features = features_reshaped.flatten()
        
        return augmented_features

    def optimize_hyperparameters(self, X_train, y_train):
        """Optimize model hyperparameters using GridSearchCV."""
        print("Optimizing hyperparameters...")
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 15, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        grid_search = GridSearchCV(
            estimator=RandomForestClassifier(random_state=42, n_jobs=-1),
            param_grid=param_grid,
            cv=3,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best cross-validation score: {grid_search.best_score_:.4f}")
        
        self.model = grid_search.best_estimator_
        
        return self.model

    def train(self):
        """Train the model and save it."""
        # Load and preprocess data
        self.X_train, self.y_train, self.X_test, self.y_test = self.load_data()
        
        # Optimize hyperparameters
        self.optimize_hyperparameters(self.X_train, self.y_train)
        
        # Train the model with best parameters
        print("Training model with best parameters...")
        self.model.fit(self.X_train, self.y_train)
        
        # Evaluate on test set
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"Test accuracy: {accuracy:.4f}")
        
        # Print classification report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred))
        
        # Save the model and scaler
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, self.model_path)
        print(f"Model saved to {self.model_path}")
        
        return self.model, self.scaler
