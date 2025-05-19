import joblib
from backend_config import ASL_MODEL_TYPE, ASL_MODELS

def load_model(model_type=None):
    """
    Load the ASL model based on configuration or provided model type.
    
    Args:
        model_type: Optional model type to load. If None, uses the configured type.
    
    Returns:
        The loaded model and scaler (if available)
    """
    if model_type is None:
        model_type = ASL_MODEL_TYPE
    model_path = ASL_MODELS[model_type]
    saved_data = joblib.load(model_path)
    
    # For custom model, we saved a dictionary with model and scaler
    if isinstance(saved_data, dict):
        return saved_data['model'], saved_data.get('scaler')
    return saved_data, None
