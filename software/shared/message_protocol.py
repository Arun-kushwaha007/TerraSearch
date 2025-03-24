"""
shared/message_protocol.py
Defines standardized message formats for communication between RPi and Laptop.
"""
import json

def create_message(sensor_type, data, timestamp=None):
    """
    Create a JSON message containing sensor data.
    sensor_type: 'lidar' or 'gpr'
    data: sensor data (string or dict)
    timestamp: optional timestamp; if not provided, use current time.
    """
    import time
    if timestamp is None:
        timestamp = time.time()
    message = {
        "sensor": sensor_type,
        "data": data,
        "timestamp": timestamp
    }
    return json.dumps(message)

def parse_message(message):
    """
    Parse a JSON message.
    Returns a dictionary or raises ValueError if parsing fails.
    """
    try:
        parsed = json.loads(message)
        return parsed
    except Exception as e:
        raise ValueError(f"Error parsing message: {e}")
