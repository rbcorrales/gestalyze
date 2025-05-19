import numpy as np
from .model_loader import load_model
from .utils import preprocess_landmarks
from backend_config import ASL_MODEL_TYPE

class ASLPredictor:
    def __init__(self):
        """Initialize the ASL predictor with both models."""
        # print(f"Initializing ASLPredictor with model type: {ASL_MODEL_TYPE}")
        # Load both models
        self.models = {}
        self.scalers = {}
        
        # Load custom model and scaler
        custom_model, custom_scaler = load_model('custom')
        self.models['custom'] = custom_model
        self.scalers['custom'] = custom_scaler
        
        # Load online model and scaler
        online_model, online_scaler = load_model('online')
        self.models['online'] = online_model
        self.scalers['online'] = online_scaler
        
        self.model_type = ASL_MODEL_TYPE
        self.model = self.models[self.model_type]
        self.scaler = self.scalers.get(self.model_type)
        
        print(f"Loaded models. Current model type: {self.model_type}")
        # print(f"Model classes: {self.model.classes_}")
    
    def update_model_type(self, model_type):
        """
        Update the model type and switch to the corresponding model.
        
        Args:
            model_type: The new model type ('custom' or 'online')
        """
        print(f"Updating model type from {self.model_type} to {model_type}")
        self.model_type = model_type
        self.model = self.models[model_type]
        self.scaler = self.scalers.get(model_type)
        # print(f"New model classes: {self.model.classes_}")
    
    def predict(self, landmarks):
        """
        Predict the ASL letter from hand landmarks.
        
        Args:
            landmarks: List of hand landmarks (21 points with x, y, z coordinates)
            
        Returns:
            str: Predicted ASL letter
        """
        # Preprocess landmarks
        features = preprocess_landmarks(landmarks, self.model_type)
        
        # Apply scaler if available
        if self.scaler is not None:
            features = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        
        # For online model, convert numeric prediction to letter using ASCII
        # For custom model, use prediction directly
        if self.model_type == 'online':
            return chr(prediction + ord('A'))
        return prediction
    
    def predict_proba(self, landmarks):
        """
        Get probability distribution over all possible ASL letters.
        
        Args:
            landmarks: List of hand landmarks (21 points with x, y, z coordinates)
            
        Returns:
            dict: Dictionary mapping ASL letters to their probabilities
        """
        # Preprocess landmarks
        features = preprocess_landmarks(landmarks, self.model_type)
        
        # Apply scaler if available
        if self.scaler is not None:
            features = self.scaler.transform(features)
        
        # Get probability distribution
        probabilities = self.model.predict_proba(features)[0]
        
        # For online model, map indices to letters using ASCII
        # For custom model, use classes directly
        if self.model_type == 'online':
            result = {chr(ord('A') + i): float(p) for i, p in enumerate(probabilities)}
        else:
            result = {str(k): float(v) for k, v in zip(self.model.classes_, probabilities)}
            
        return result
