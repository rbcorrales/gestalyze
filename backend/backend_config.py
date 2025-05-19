"""Backend-specific configuration."""

import os

# ==========================================
# WebSocket configuration
# ==========================================
WEBSOCKET_HOST = "0.0.0.0"
WEBSOCKET_PORT = 8000

# ==========================================
# CORS configuration
# ==========================================
CORS_CONFIG = {
    "allow_origins": ["*"],  # In production, replace with specific origins
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

# ==========================================
# Image saving configuration (for debugging)
# ==========================================
SAVE_IMAGES = False
SAVE_DIR = "saved_images"

# ==========================================
# ASL Recognition configuration
# ==========================================
ENABLE_ASL_PREDICTION = False
ASL_MODEL_TYPE = "online"  # "custom" or "online"
ASL_MODELS = {
    "custom": os.path.join("models", "custom_handsignimages.joblib"),
    "online": os.path.join("models", "online_marxulia_asl_sign_languages_alphabets_v03.joblib")
}
