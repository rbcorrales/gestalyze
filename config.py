"""Global shared configuration for the Gestalyze application."""

# =============================
# MQTT configuration
# =============================
MQTT_CONFIG = {
    "broker": "localhost",  # MQTT broker address
    "port": 1883,          # MQTT broker port
    "client_id": "gestalyze_backend",
    "username": "gestalyze",  # MQTT username
    "password": "gestalyze123",  # MQTT password
    "topics": {
        "gesture_recognized": "gestalyze/gesture/recognized",
        "hand_status": "gestalyze/hand/status"
    }
}
