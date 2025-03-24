"""
rpi/config.py
Configuration settings for Raspberry Pi
"""
# Network Configuration
LAPTOP_IP = "192.168.1.100"      # Update with your laptop IP address
MQTT_PORT = 1883                 # Default MQTT port

# Serial Port Settings for Sensors
LIDAR_PORT = "/dev/ttyUSB1"      # LiDAR serial port
GPR_PORT = "/dev/ttyUSB2"        # GPR serial port
SERIAL_BAUDRATE = 115200         # Baud rate for both sensors

# Drone Control Parameters
DEFAULT_TAKEOFF_ALTITUDE = 20    # Meters
DEFAULT_SPEED = 10               # Meters per second

# MQTT Topics
MQTT_DATA_TOPIC = "drone/data"
MQTT_COMMAND_TOPIC = "drone/commands"

# Other Settings
SENSOR_READ_TIMEOUT = 2          # Seconds before retrying sensor read
