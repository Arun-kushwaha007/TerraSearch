"""
laptop/main.py
Main processing loop: subscribes to sensor data, processes it, and sends control commands.
"""
import time
import json
import logging
import threading
import numpy as np
import paho.mqtt.client as mqtt

from laptop import config
from laptop.receiver import setup_receiver
from laptop.lidar_processing import process_lidar_data, detect_obstacles
from laptop.gpr_processing import process_gpr_data, detect_anomalies
from laptop.drone_commands import send_drone_command

logger = logging.getLogger("LaptopMain")
logger.setLevel(logging.INFO)

# Shared dictionary to hold the latest sensor data
shared_data = {"latest_data": None}

def analyze_and_decide():
    """
    Analyze the sensor data and decide what drone command to send.
    For example, if GPR anomalies are detected, command drone to hover.
    """
    data = shared_data.get("latest_data", None)
    if data is None:
        logger.warning("No sensor data available for analysis")
        return

    try:
        lidar_raw = data.get("lidar", "")
        gpr_raw = data.get("gpr", "")
        lidar_points = process_lidar_data(lidar_raw)
        obstacles = detect_obstacles(lidar_points, threshold=0.5)
        
        gpr_data = process_gpr_data(gpr_raw)
        anomalies = detect_anomalies(gpr_data, threshold=0.8)
        
        # Decision logic: if any anomalies found, hover; otherwise, continue moving forward.
        if anomalies:
            decision = {"action": "hover"}
            logger.info("Anomaly detected: sending hover command")
        elif obstacles:
            decision = {"action": "move", "direction": "backward", "speed": 5}
            logger.info("Obstacle detected: moving backward")
        else:
            decision = {"action": "move", "direction": "forward", "speed": 10}
            logger.info("No obstacles: moving forward")
            
        send_drone_command(decision)
    except Exception as e:
        logger.error(f"Error in decision analysis: {e}")

def main():
    # Setup MQTT receiver for sensor data
    client = setup_receiver(shared_data)
    client_thread = threading.Thread(target=client.loop_forever, daemon=True)
    client_thread.start()
    
    logger.info("Laptop main loop started. Waiting for sensor data...")
    try:
        while True:
            analyze_and_decide()
            time.sleep(2)  # Frequency of analysis can be adjusted
    except KeyboardInterrupt:
        logger.info("Shutdown signal received. Exiting main loop.")

if __name__ == "__main__":
    main()
