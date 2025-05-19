from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import base64
import os
from datetime import datetime
from io import BytesIO
import cv2
import numpy as np
import mediapipe as mp
from config import MQTT_CONFIG
from backend_config import (
    SAVE_IMAGES, SAVE_DIR, CORS_CONFIG, ENABLE_ASL_PREDICTION,
    ASL_MODEL_TYPE
)
from inference.predict import ASLPredictor
from inference.utils import extract_landmarks_from_mediapipe
from inference.model_loader import load_model
from mqtt.mqtt_client import MQTTClient
from collections import deque
from threading import Lock

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG["allow_origins"],
    allow_credentials=CORS_CONFIG["allow_credentials"],
    allow_methods=CORS_CONFIG["allow_methods"],
    allow_headers=CORS_CONFIG["allow_headers"],
)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.3,
    model_complexity=1
)

# Initialize ASL predictor
asl_predictor = ASLPredictor()

# Create directory for saved images if saving is enabled
if SAVE_IMAGES:
    os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize MQTT client
mqtt_client = MQTTClient(
    host=MQTT_CONFIG["broker"],
    port=MQTT_CONFIG["port"],
    username=MQTT_CONFIG["username"],
    password=MQTT_CONFIG["password"]
)

# Connect to MQTT broker
mqtt_client.connect()

# Debouncing configuration
DEBOUNCE_TIME = 0.5  # seconds (reduced from 1.5)
last_gesture_data = None
last_update_time = 0
gesture_history = deque(maxlen=10)  # Store recent gesture data
gesture_lock = Lock()  # Lock for thread safety

# Add this variable at the top level with the other debouncing variables
HAND_TIMEOUT = 1.0  # seconds to wait before resetting when no hands are detected (reduced from 5.0)
last_reset_time = 0  # Track when we last sent a reset
RESET_COOLDOWN = 5.0  # Minimum seconds between resets
sensors_reset = False  # Track if sensors are currently in reset state

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive the data as JSON
            data = await websocket.receive_json()
            
            # Handle ASL toggle command and model type changes
            if "enable_asl" in data:
                global ENABLE_ASL_PREDICTION
                ENABLE_ASL_PREDICTION = data["enable_asl"]
                continue
            if "model_type" in data:
                global ASL_MODEL_TYPE
                ASL_MODEL_TYPE = data["model_type"]
                asl_predictor.update_model_type(ASL_MODEL_TYPE)
                continue
                
            if "image" not in data:
                continue
                
            # Process image data
            image_data = data["image"].split(",")[1]
            image_bytes = base64.b64decode(image_data)
            
            # Convert to OpenCV format
            nparr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Process the frame with MediaPipe
            results = hands_detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            hand_detected = False
            finger_count = 0
            lifted_fingers = []
            handedness_label = None
            asl_letter = None
            asl_probabilities = None
            
            if results.multi_hand_landmarks:
                hand_detected = True
                
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks on the frame
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
                    )
                    
                    # Count fingers and get handedness
                    handedness_label = get_corrected_handedness(results)
                    finger_count, lifted_fingers = count_fingers(hand_landmarks, handedness_label)
                    
                    # Extract landmarks and predict ASL letter if enabled
                    if ENABLE_ASL_PREDICTION:
                        landmarks = extract_landmarks_from_mediapipe(hand_landmarks)
                        asl_letter = asl_predictor.predict(landmarks)
                        asl_probabilities = asl_predictor.predict_proba(landmarks)
                    
                    # Get hand view for MQTT
                    hand_view = get_hand_view(hand_landmarks, handedness_label)
                    
                    # Publish hand status via MQTT
                    mqtt_client.publish_hand_status(
                        hand=handedness_label,
                        orientation=hand_view,
                        extended_fingers=lifted_fingers
                    )
                    
                    # If ASL prediction is enabled and we have a prediction, publish via MQTT
                    if ENABLE_ASL_PREDICTION and asl_letter:
                        mqtt_client.publish_gesture_event(
                            gesture=asl_letter,
                            confidence=asl_probabilities[asl_letter] if asl_probabilities else 0.0,
                            hand=handedness_label,
                            orientation=hand_view,
                            extended_fingers=lifted_fingers
                        )
                    
                    # Save frame with landmarks if enabled
                    if SAVE_IMAGES:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                        save_path = os.path.join(SAVE_DIR, f"hand_{timestamp}.jpg")
                        cv2.imwrite(save_path, frame)
            
            # Convert frame back to base64 for sending
            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            
            # Prepare response data
            response_data = {
                "image_with_landmarks": f"data:image/jpeg;base64,{img_base64}",
                "hand_detected": hand_detected,
                "finger_count": finger_count,
                "hand_view": get_hand_view(hand_landmarks, handedness_label) if hand_detected else None,
                "handedness": handedness_label if hand_detected else None,
                "lifted_fingers": lifted_fingers
            }
            
            # Add ASL prediction data if enabled
            if ENABLE_ASL_PREDICTION:
                response_data.update({
                    "asl_letter": asl_letter,
                    "asl_probabilities": asl_probabilities
                })
            
            # Send response
            await websocket.send_json(response_data)
            
    except Exception as e:
        print(f"Error in websocket connection: {e}")
    finally:
        await websocket.close()


# Mount static files AFTER registering the WebSocket route
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/dist"))
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static") 


def count_fingers(hand_landmarks, handedness_label):
    """
    Count extended fingers based on hand landmarks, corrected handedness,
    and hand view ('palm' or 'back').
    """
    count = 0
    lifted_fingers = []
    if hand_landmarks:
        hand_view = get_hand_view(hand_landmarks, handedness_label)
        # print(f"Hand: {handedness_label}, View: {hand_view}")

        thumb_tip = hand_landmarks.landmark[4]
        thumb_ip = hand_landmarks.landmark[3]

        if handedness_label == "left":  # Changed to lowercase
            if hand_view == "back":  # Changed to lowercase
                if thumb_tip.x > thumb_ip.x:
                    count += 1
            else:
                if thumb_tip.x < thumb_ip.x:
                    count += 1
        elif handedness_label == "right":  # Changed to lowercase
            if hand_view == "back":  # Changed to lowercase
                if thumb_tip.x < thumb_ip.x:
                    count += 1
            else:
                if thumb_tip.x > thumb_ip.x:
                    count += 1

        if count == 1:
            lifted_fingers.append(0)  # Keep original 0-based indexing

        # Other fingers
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        for tip_idx, pip_idx in zip(tips, pips):
            tip_y = hand_landmarks.landmark[tip_idx].y
            pip_y = hand_landmarks.landmark[pip_idx].y

            if tip_y < pip_y:
                count += 1
                # Keep original 0-based indexing
                lifted_fingers.append(tip_idx / 4 - 1)
        # print(f"Fingers counted: {count}")

    return count, lifted_fingers

def get_corrected_handedness(results):
    """
    Flip handedness label if camera feed is mirrored.
    """
    label = results.multi_handedness[0].classification[0].label
    if label == "Left":
        return "right"
    elif label == "Right":
        return "left"
    return label.lower()


def get_hand_view(hand_landmarks, corrected_label):
    """
    Determine if the palm or back of the hand is facing the camera
    based on WRIST and THUMB_CMC x-positions.
    """
    wrist = hand_landmarks.landmark[0]
    thumb_cmc = hand_landmarks.landmark[1]
    x_diff = thumb_cmc.x - wrist.x

    if corrected_label == "left":
        return "back" if x_diff > 0 else "palm"
    elif corrected_label == "right":
        return "back" if x_diff < 0 else "palm"
    return "palm"
