"""
laptop/drone_commands.py
Sends control commands to the Raspberry Pi for drone operation.
"""
import json
import logging
import paho.mqtt.client as mqtt
from laptop import config

logger = logging.getLogger("DroneCommands")
logger.setLevel(logging.INFO)

def send_drone_command(command_dict):
    """
    Publishes a command dictionary to the MQTT command topic.
    Expected command_dict format:
    {
        "action": "takeoff"/"land"/"move"/"hover",
        "altitude": <value>,          # optional, for takeoff
        "direction": <value>,         # optional, for move
        "speed": <value>              # optional, for move
    }
    """
    try:
        client = mqtt.Client()
        client.connect(config.BROKER_IP, config.MQTT_PORT, keepalive=60)
        payload = json.dumps(command_dict)
        client.publish(config.MQTT_COMMAND_TOPIC, payload)
        client.disconnect()
        logger.info(f"Sent drone command: {payload}")
    except Exception as e:
        logger.error(f"Error sending drone command: {e}")

# For testing purposes, you can call this function with a test command.
if __name__ == "__main__":
    test_command = {"action": "hover"}
    send_drone_command(test_command)
