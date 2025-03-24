"""
laptop/config.py
Configuration settings for the laptop
"""
# MQTT Broker settings
BROKER_IP = "192.168.1.100"    # Update with the RPI's IP or the MQTT broker IP
MQTT_PORT = 1883

# MQTT Topics (should match rpi/config.py)
MQTT_DATA_TOPIC = "drone/data"
MQTT_COMMAND_TOPIC = "drone/commands"
