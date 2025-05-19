"""Global configuration package for Gestalyze application."""

# MQTT configuration
MQTT_CONFIG = {
    "broker": "localhost",
    "port": 1883,
    "client_id": "gestalyze_backend", 
    "username": "gestalyze",
    "password": "gestalyze_password",
    "topics": {
        "gesture_recognized": "gestalyze/gesture/recognized",
        "hand_status": "gestalyze/hand/status"
    }
}
