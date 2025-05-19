import json
import logging
import websocket
from typing import Dict, Any, Optional
from plugin_config import HOME_ASSISTANT_CONFIG

logger = logging.getLogger(__name__)

class HAClient:
    """Home Assistant WebSocket client for Gestalyze."""
    
    def __init__(self, host: str, access_token: str):
        """Initialize the Home Assistant client."""
        self.host = host
        self.access_token = access_token
        self.websocket = None
        self.message_id = 0

    def connect(self):
        """Connect to Home Assistant WebSocket API."""
        try:
            # print(f"Connecting to Home Assistant at {self.host} with token {self.token}")
            url = f"ws://{self.host}/api/websocket"
            self.websocket = websocket.create_connection(url, timeout=10)  # Add a timeout
            
            # First, receive the auth_required message from the server
            initial_response = json.loads(self.websocket.recv())
            logger.debug("Initial response: %s", initial_response)
            
            if initial_response.get("type") != "auth_required":
                logger.error("Unexpected initial response: %s", initial_response)
                raise Exception("Unexpected initial response from Home Assistant")
            
            # Authentication message
            auth_msg = {
                "type": "auth",
                "access_token": self.access_token
            }
            self.websocket.send(json.dumps(auth_msg))
            
            # Check authentication response
            response = json.loads(self.websocket.recv())
            logger.debug("Authentication response: %s", response)
            if response.get("type") != "auth_ok":
                logger.error("Authentication failed: %s", response)
                raise Exception("Authentication failed")
            
            logger.info("Connected to Home Assistant")
            
        except Exception as e:
            logger.error(f"Error connecting to Home Assistant: {e}")
            self.websocket = None  # Reset the connection
            raise  # Re-raise the exception

    def update_gesture_state(self, data: Dict[str, Any]):
        """Update Gestalyze sensor states.
        
        Args:
            data: Dictionary containing sensor states
                {
                    "hand": "left"/"right",
                    "orientation": "palm"/"back",
                    "fingers": "comma,separated,list",
                    "finger_count": int
                }
        """
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if not self.websocket:
                    print("WebSocket not connected, attempting to connect...")
                    self.connect()
                
                message = {
                    "id": self.message_id,
                    "type": "call_service",
                    "domain": "gestalyze",
                    "service": "set_gesture_state",
                    "service_data": data
                }
                
                print(f"Sending to HA: {json.dumps(message)}")
                self.websocket.send(json.dumps(message))
                self.message_id += 1
                logger.info("Successfully sent gesture state to Home Assistant")
                return  # Success, exit the method
                
            except (BrokenPipeError, websocket.WebSocketConnectionClosedException) as e:
                logger.warning(f"Connection error: {e}. Attempting to reconnect...")
                self.websocket = None  # Reset the connection
                retry_count += 1
                
                if retry_count >= max_retries:
                    logger.error("Failed to send gesture state after multiple attempts")
                    raise  # Re-raise the exception after all retries are exhausted
                
                # Wait a bit before retrying
                import time
                time.sleep(1)

    def close(self):
        """Close the WebSocket connection."""
        if self.websocket:
            self.websocket.close()

    def authenticate(self):
        """Check if the authentication was successful."""
        # First, receive the auth_required message from the server
        initial_response = json.loads(self.websocket.recv())
        logger.debug("Initial response: %s", initial_response)
        
        if initial_response.get("type") != "auth_required":
            logger.error("Unexpected initial response: %s", initial_response)
            return False
        
        # Authentication message
        auth_msg = {
            "type": "auth",
            "access_token": self.access_token
        }
        self.websocket.send(json.dumps(auth_msg))
        
        # Check authentication response
        result = json.loads(self.websocket.recv())
        logger.debug("Authentication response: %s", result)
        if result.get("type") == "auth_ok":
            return True
        else:
            logger.error("Authentication failed: %s", result)
            return False

    def trigger_event(self, event_type: str, event_data: Dict[str, Any]):
        """Trigger a custom event in Home Assistant.
        
        Args:
            event_type: The type of event to trigger (e.g., "gestalyze_gesture_detected")
            event_data: Dictionary containing event data to be sent as payload
        """
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if not self.websocket:
                    print("WebSocket not connected, attempting to connect...")
                    self.connect()
                
                # Ensure event_data is a dictionary and not empty
                if not isinstance(event_data, dict):
                    event_data = {"data": event_data}
                
                message = {
                    "id": self.message_id,
                    "type": "fire_event",
                    "event_type": event_type,
                    "event_data": event_data
                }
                
                logger.debug(f"Triggering event in HA: {json.dumps(message)}")
                self.websocket.send(json.dumps(message))
                print(f"Sent to HA: {json.dumps(message)}")
                
                # Wait for a response to confirm the event was received
                response = json.loads(self.websocket.recv())
                logger.debug(f"Event trigger response: {response}")
                
                # Increment the ID counter regardless of the response
                self.message_id += 1
                
                # Check if the event was successfully fired
                if response.get("type") == "result" and response.get("success", False):
                    logger.info(f"Successfully triggered event {event_type} in Home Assistant")
                    return  # Success, exit the method
                else:
                    logger.warning(f"Failed to trigger event: {response}")
                    # Don't retry on non-connection errors
                    if not isinstance(response.get("error", {}).get("code"), str):
                        return
                
            except (BrokenPipeError, websocket.WebSocketConnectionClosedException) as e:
                logger.warning(f"Connection error: {e}. Attempting to reconnect...")
                self.websocket = None  # Reset the connection
                retry_count += 1
                
                if retry_count >= max_retries:
                    logger.error("Failed to trigger event after multiple attempts")
                    raise  # Re-raise the exception after all retries are exhausted
                
                # Wait a bit before retrying
                import time
                time.sleep(1)
