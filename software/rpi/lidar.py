"""
rpi/lidar.py
Interface for reading LiDAR sensor data.
Provides a robust reader that reconnects on errors.
"""
import serial
import time
import logging
from rpi import config

logger = logging.getLogger("LiDAR")
logger.setLevel(logging.INFO)

class LidarReader:
    def __init__(self, port=config.LIDAR_PORT, baudrate=config.SERIAL_BAUDRATE, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connect()

    def connect(self):
        """Establish serial connection."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logger.info(f"Connected to LiDAR on {self.port} at {self.baudrate}bps")
        except Exception as e:
            logger.error(f"Failed to connect to LiDAR on {self.port}: {e}")
            self.ser = None

    def read_data(self):
        """Read one line of data from the LiDAR sensor.
           Returns a string with sensor data or None if failed.
        """
        if self.ser is None or not self.ser.is_open:
            logger.warning("LiDAR serial connection not available. Attempting reconnect...")
            self.connect()
            if self.ser is None:
                return None

        try:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                logger.debug(f"Raw LiDAR data: {line}")
                return line
            else:
                logger.warning("Empty LiDAR data received")
                return None
        except Exception as e:
            logger.error(f"Error reading LiDAR data: {e}")
            return None

# For ease of use, provide a module-level function
def get_lidar_data():
    reader = LidarReader()
    start_time = time.time()
    while time.time() - start_time < config.SENSOR_READ_TIMEOUT:
        data = reader.read_data()
        if data is not None:
            return data
        time.sleep(0.1)
    logger.error("Timeout reading LiDAR data")
    return ""
