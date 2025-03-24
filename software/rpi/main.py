"""
rpi/main.py
Main script for the Raspberry Pi.
Reads sensor data from LiDAR and GPR, then publishes to the laptop via MQTT.
Also subscribes for incoming drone commands.
"""
import time
import json
import logging
import threading
import paho.mqtt.client as mqtt

from rpi import config
from rpi.lidar import get_lidar_data
from rpi.gpr import get_gpr_data
from rpi.drone_control import connect_drone, takeoff, land, move

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RPI_Main")

# Global flag for shutdown
shutdown_flag = False

def on_command(client, userdata, message):
    """Callback for processing incoming drone commands."""
    try:
        command = json.loads(message.payload.decode())
        logger.info(f"Received command: {command}")
        # Connect to drone if not already connected; for production, consider caching connection
        drone = connect_drone()
        if command.get("action") == "takeoff":
            takeoff(drone, command.get("altitude", config.DEFAULT_TAKEOFF_ALTITUDE))
        elif command.get("action") == "land":
            land(drone)
        elif command.get("action") == "move":
            move(drone, direction=command.get("direction", "forward"), speed=command.get("speed", config.DEFAULT_SPEED))
        else:
            logger.warning("Unknown command received")
    except Exception as e:
        logger.error(f"Error processing command: {e}")

def sensor_data_loop(mqtt_client):
    """Continuously read sensor data and publish via MQTT."""
    while not shutdown_flag:
        try:
            lidar_data = get_lidar_data()
            gpr_data = get_gpr_data()
            payload = {
                "lidar": lidar_data,
                "gpr": gpr_data,
                "timestamp": time.time()
            }
            mqtt_client.publish(config.MQTT_DATA_TOPIC, json.dumps(payload))
            logger.info(f"Published sensor data: {payload}")
        except Exception as e:
            logger.error(f"Error in sensor loop: {e}")
        time.sleep(1)  # Adjust frequency as needed

def main():
    try:
        mqtt_client = mqtt.Client("RaspberryPi")
        mqtt_client.connect(config.LAPTOP_IP, config.MQTT_PORT, keepalive=60)
        mqtt_client.subscribe(config.MQTT_COMMAND_TOPIC)
        mqtt_client.on_message = on_command
        
        # Run sensor loop in a separate thread
        sensor_thread = threading.Thread(target=sensor_data_loop, args=(mqtt_client,), daemon=True)
        sensor_thread.start()
        
        logger.info("Raspberry Pi main loop started. Waiting for commands...")
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")

if __name__ == "__main__":
    main()
