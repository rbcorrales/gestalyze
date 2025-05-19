from abc import ABC, abstractmethod
import joblib
import os
from sklearn.metrics import accuracy_score, classification_report

class BaseTrainer(ABC):
    def __init__(self, model_name, model_path):
        self.model_name = model_name
        self.model_path = model_path
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.model = None
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    @abstractmethod
    def load_data(self):
        """Load and preprocess the training data."""
        pass
    
    @abstractmethod
    def preprocess_features(self, landmarks):
        """Preprocess hand landmarks for model input."""
        pass
    
    def train(self):
        """Train the model and save it."""
        # Load and preprocess data
        self.X_train, self.y_train, self.X_test, self.y_test = self.load_data()
        
        # Train the model
        self.model.fit(self.X_train, self.y_train)
        
        # Save the model
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")
    
    def evaluate(self):
        """Evaluate the model's performance."""
        if self.X_test is None or self.y_test is None:
            raise ValueError("Test data not available. Run train() first.")
            
        # Make predictions
        y_pred = self.model.predict(self.X_test)
        
        # Calculate accuracy
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"\nAccuracy: {accuracy:.4f}")
        
        # Print classification report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred))
    
    def load_model(self):
        """Load a trained model."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            return True
        return False
