"""
rpi/drone_control.py
Controls drone movement via MAVLink.
Includes functions for connecting, takeoff, landing, and sending commands.
"""
import time
import logging
from pymavlink import mavutil
from rpi import config

logger = logging.getLogger("DroneControl")
logger.setLevel(logging.INFO)

def connect_drone(connection_str="udp:0.0.0.0:14550", retry_interval=5, max_retries=5):
    """Connect to the drone via MAVLink with retries."""
    retries = 0
    while retries < max_retries:
        try:
            drone = mavutil.mavlink_connection(connection_str)
            drone.wait_heartbeat(timeout=10)
            logger.info("Drone connected via MAVLink")
            return drone
        except Exception as e:
            logger.error(f"Drone connection failed: {e}. Retrying in {retry_interval}s...")
            time.sleep(retry_interval)
            retries += 1
    raise ConnectionError("Unable to connect to drone after multiple attempts.")

def takeoff(drone, altitude=config.DEFAULT_TAKEOFF_ALTITUDE):
    """Send takeoff command to drone."""
    try:
        drone.mav.command_long_send(
            drone.target_system,
            drone.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0, 0, 0, 0, 0, 0, 0, altitude
        )
        logger.info(f"Takeoff command sent to reach altitude {altitude}m")
    except Exception as e:
        logger.error(f"Failed to send takeoff command: {e}")

def land(drone):
    """Send landing command to drone."""
    try:
        drone.mav.command_long_send(
            drone.target_system,
            drone.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND,
            0, 0, 0, 0, 0, 0, 0, 0
        )
        logger.info("Landing command sent")
    except Exception as e:
        logger.error(f"Failed to send landing command: {e}")

def move(drone, direction="forward", speed=config.DEFAULT_SPEED):
    """Send movement command based on direction and speed.
       This is a placeholder function; implementation will depend on your flight controller.
    """
    try:
        # Example command: sending a text-based command via MAVLink message
        command_str = f"MOVE {direction.upper()} {speed}"
        drone.mav.statustext_send(command_str.encode())
        logger.info(f"Move command sent: {command_str}")
    except Exception as e:
        logger.error(f"Failed to send move command: {e}")
