import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("gestalyze/#")

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

def main():
    # Create MQTT client
    client = mqtt.Client(client_id="test_client")
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to broker
    print("Connecting to MQTT broker...")
    client.connect("localhost", 1883)
    client.loop_start()

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping MQTT test client...")
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main() 
