"""
laptop/receiver.py
Handles incoming sensor data from Raspberry Pi.
This module uses a callback to process messages and passes them to a handler.
"""
import json
import logging
import paho.mqtt.client as mqtt
from laptop import config

logger = logging.getLogger("Receiver")
logger.setLevel(logging.INFO)

def process_incoming_data(data):
    """
    Process the incoming sensor data.
    This function can be extended to include advanced processing.
    """
    try:
        # Example: Simply log the data; further processing done in main loop
        logger.info(f"Processing data: {data}")
        return data
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        return None

def on_message(client, userdata, message):
    """MQTT callback when sensor data is received."""
    try:
        payload = json.loads(message.payload.decode())
        logger.info(f"Received data: {payload}")
        processed = process_incoming_data(payload)
        if processed:
            userdata["latest_data"] = processed
    except Exception as e:
        logger.error(f"Failed to process incoming message: {e}")

def setup_receiver(client_userdata=None):
    """Setup the MQTT receiver client."""
    client = mqtt.Client(userdata=client_userdata)
    client.on_message = on_message
    client.connect(config.BROKER_IP, config.MQTT_PORT, keepalive=60)
    client.subscribe(config.MQTT_DATA_TOPIC)
    return client

if __name__ == "__main__":
    # For testing receiver separately
    userdata = {"latest_data": None}
    client = setup_receiver(userdata)
    client.loop_forever()
