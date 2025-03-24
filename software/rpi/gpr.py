"""
rpi/gpr.py
Interface for reading GPR sensor data.
Includes reconnection and error-handling logic.
"""
import serial
import time
import logging
from rpi import config

logger = logging.getLogger("GPR")
logger.setLevel(logging.INFO)

class GprReader:
    def __init__(self, port=config.GPR_PORT, baudrate=config.SERIAL_BAUDRATE, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connect()

    def connect(self):
        """Establish serial connection."""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            logger.info(f"Connected to GPR on {self.port} at {self.baudrate}bps")
        except Exception as e:
            logger.error(f"Failed to connect to GPR on {self.port}: {e}")
            self.ser = None

    def read_data(self):
        """Read one line of data from the GPR sensor.
           Returns a string with sensor data or None if failed.
        """
        if self.ser is None or not self.ser.is_open:
            logger.warning("GPR serial connection not available. Attempting reconnect...")
            self.connect()
            if self.ser is None:
                return None

        try:
            line = self.ser.readline().decode('utf-8').strip()
            if line:
                logger.debug(f"Raw GPR data: {line}")
                return line
            else:
                logger.warning("Empty GPR data received")
                return None
        except Exception as e:
            logger.error(f"Error reading GPR data: {e}")
            return None

def get_gpr_data():
    reader = GprReader()
    start_time = time.time()
    while time.time() - start_time < config.SENSOR_READ_TIMEOUT:
        data = reader.read_data()
        if data is not None:
            return data
        time.sleep(0.1)
    logger.error("Timeout reading GPR data")
    return ""
