import json
import logging
import paho.mqtt.client as mqtt
from typing import Dict, Any, List
from datetime import datetime
from ha_client import HAClient
from config import MQTT_CONFIG
from plugin_config import HOME_ASSISTANT_CONFIG
from rich.console import Console
from rich.json import JSON

console = Console()

logger = logging.getLogger(__name__)

class GestalyzePlugin:
    """Home Assistant plugin for Gestalyze gesture recognition."""
    
    def __init__(self):
        """Initialize the plugin."""
        # Get configuration from config files
        self.mqtt_broker = MQTT_CONFIG["broker"]
        self.mqtt_port = MQTT_CONFIG["port"]
        self.mqtt_username = MQTT_CONFIG["username"]
        self.mqtt_password = MQTT_CONFIG["password"]
        self.ha_host = HOME_ASSISTANT_CONFIG["host"]
        self.access_token = HOME_ASSISTANT_CONFIG["access_token"]
        
        # Initialize MQTT client
        self.mqtt_client = mqtt.Client(client_id="gestalyze_ha_plugin")
        self.mqtt_client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_message = self._on_mqtt_message
        
        # Initialize Home Assistant WebSocket client
        self.ha_client = HAClient(self.ha_host, self.access_token)
        
        # Initialize entities
        self.entities = {
            "hand": None,
            "orientation": None,
            "fingers": None,
            "finger_count": None
        }

    def start(self):
        """Start the plugin."""
        try:
            # Connect to MQTT broker
            self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port)
            self.mqtt_client.loop_start()
            
            # Subscribe to topics
            self.mqtt_client.subscribe(MQTT_CONFIG["topics"]["gesture_recognized"])
            self.mqtt_client.subscribe(MQTT_CONFIG["topics"]["hand_status"])
            
            # Connect to Home Assistant
            self.ha_client.connect()
            
            logger.info("Gestalyze plugin started successfully")
        except Exception as e:
            logger.error(f"Failed to start Gestalyze plugin: {e}")
            raise

    def stop(self):
        """Stop the plugin."""
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        logger.info("Gestalyze plugin stopped")

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """Callback for when MQTT client connects."""
        if rc == 0:
            logger.info("Connected to MQTT broker")
        elif rc == 5:
            logger.error("Authentication failed - invalid username or password")
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")

    def _on_mqtt_message(self, client, userdata, msg):
        """Callback for when MQTT message is received."""
        try:
            payload = json.loads(msg.payload.decode())
            topic = msg.topic
            
            if topic == MQTT_CONFIG["topics"]["gesture_recognized"]:
                self._handle_gesture_event(payload)
            elif topic == MQTT_CONFIG["topics"]["hand_status"]:
                self._handle_hand_status(payload)
                
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    def _format_finger_data(self, extended_fingers: List[float]) -> Dict[str, Any]:
        """Format finger data for Home Assistant."""
        # Convert float values to strings and join with commas
        fingers_str = ",".join(str(int(f)) for f in extended_fingers)
        return {
            "fingers": fingers_str,
            "finger_count": len(extended_fingers)
        }

    def _handle_gesture_event(self, payload: Dict[str, Any]):
        """Handle gesture recognition events."""
        try:
            # Format finger data
            finger_data = self._format_finger_data(payload["extended_fingers"])
            
            # Format data for Home Assistant
            ha_data = {
                "hand": payload["hand"],
                "orientation": payload["orientation"],
                **finger_data
            }
            
            # Update Home Assistant entities
            self._update_ha_entities(ha_data)
            
            # Add gesture-specific data for the event
            event_data = {
                "gesture": payload["gesture"],
                "confidence": float(payload["confidence"]),  # Ensure confidence is a float
                **ha_data  # Include all sensor data in the event
            }
            
            # Trigger Home Assistant event
            self._trigger_ha_event("gestalyze_gesture_recognized", event_data)
            
            logger.debug(f"Processed gesture event: {event_data}")
        except Exception as e:
            logger.error(f"Error handling gesture event: {e}")

    def _handle_hand_status(self, payload: Dict[str, Any]):
        """Handle hand status updates."""
        try:
            # Format finger data
            finger_data = self._format_finger_data(payload["extended_fingers"])
            
            # Format data for Home Assistant
            ha_data = {
                "hand": payload["hand"],
                "orientation": payload["orientation"],
                **finger_data
            }
            
            # Update Home Assistant entities
            self._update_ha_entities(ha_data)
            
            # Trigger Home Assistant event with the same data
            self._trigger_ha_event("gestalyze_hand_status_updated", ha_data)
            
            logger.debug(f"Processed hand status update: {ha_data}")
        except Exception as e:
            logger.error(f"Error handling hand status update: {e}")

    def _update_ha_entities(self, data: Dict[str, Any]):
        """Update all Home Assistant entities."""
        try:
            # Update the state in Home Assistant using the service
            self.ha_client.update_gesture_state(data)
            
            logger.debug(f"Updated Home Assistant entities with data: {data}")
        except Exception as e:
            logger.error(f"Error updating Home Assistant entities: {e}")

    def _trigger_ha_event(self, event_type: str, event_data: Dict[str, Any]):
        """Trigger a Home Assistant event."""
        try:
            console.print(f"[bold magenta]🎯 Publishing HA event:[/bold magenta] [cyan]{event_type}[/cyan]")
            console.print(JSON.from_data(event_data))
            self.ha_client.trigger_event(event_type, event_data)
        except Exception as e:
            logger.error(f"Error triggering Home Assistant event: {e}")

def main():
    """Main entry point for the plugin."""
    plugin = GestalyzePlugin()
    
    try:
        plugin.start()
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        plugin.stop()
    except Exception as e:
        logger.error(f"Plugin error: {e}")
        plugin.stop()

if __name__ == "__main__":
    main()
