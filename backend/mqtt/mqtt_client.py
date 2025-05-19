import json
import logging
import paho.mqtt.client as mqtt
from typing import Dict, Any, Callable
from datetime import datetime

logger = logging.getLogger(__name__)

class MQTTClient:
    """MQTT client for publishing gesture events and hand status updates."""
    
    def __init__(self, host: str = "localhost", port: int = 1883, 
                 username: str = None, password: str = None):
        """Initialize the MQTT client.
        
        Args:
            host: MQTT broker host
            port: MQTT broker port
            username: MQTT username
            password: MQTT password
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connected = False
        
        # Create MQTT client with a specific client ID
        self.client = mqtt.Client(client_id="gestalyze_backend")
        
        # Set username and password
        self.client.username_pw_set(username, password)
        
        # Set up callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        
        # Set up TLS if needed
        if self.port == 8883:
            self.client.tls_set()

    def connect(self):
        """Connect to the MQTT broker."""
        try:
            self.client.connect(self.host, self.port)
            self.client.loop_start()
            logger.info(f"Connected to MQTT broker at {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()
        logger.info("Disconnected from MQTT broker")

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            self.connected = True
            logger.info("Connected to MQTT broker")
        elif rc == 5:
            logger.error("Authentication failed - invalid username or password")
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker."""
        self.connected = False
        if rc != 0:
            logger.warning(f"Unexpected disconnection from MQTT broker with code: {rc}")

    def _on_message(self, client, userdata, message):
        """Callback for when a message is received from the broker."""
        # This method is not used in the current implementation
        pass

    def publish_gesture_event(self, gesture: str, confidence: float, hand: str, 
                            orientation: str, extended_fingers: list):
        """Publish a gesture recognition event.
        
        Args:
            gesture: The recognized gesture
            confidence: Confidence score of the recognition
            hand: Which hand was used (left/right)
            orientation: Hand orientation
            extended_fingers: List of extended fingers
        """
        if not self.connected:
            logger.warning("Not connected to MQTT broker, cannot publish gesture event")
            return

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "gesture": gesture,
            "confidence": confidence,
            "hand": hand,
            "orientation": orientation,
            "extended_fingers": extended_fingers
        }

        try:
            self.client.publish(f"{self.username}/gesture/recognized", json.dumps(payload))
            logger.debug(f"Published gesture event: {payload}")
        except Exception as e:
            logger.error(f"Failed to publish gesture event: {e}")

    def publish_hand_status(self, hand: str, orientation: str, extended_fingers: list):
        """Publish hand status updates.
        
        Args:
            hand: Which hand is being tracked
            orientation: Current hand orientation
            extended_fingers: List of currently extended fingers
        """
        if not self.connected:
            logger.warning("Not connected to MQTT broker, cannot publish hand status")
            return

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "hand": hand,
            "orientation": orientation,
            "extended_fingers": extended_fingers
        }

        try:
            self.client.publish(f"{self.username}/hand/status", json.dumps(payload))
            logger.debug(f"Published hand status: {payload}")
        except Exception as e:
            logger.error(f"Failed to publish hand status: {e}")
