"""
laptop/lidar_processing.py
Processes raw LiDAR sensor data and extracts useful information.
"""
import numpy as np
import logging

logger = logging.getLogger("LidarProcessing")
logger.setLevel(logging.INFO)

def process_lidar_data(lidar_raw):
    """
    Convert comma-separated string of LiDAR readings to a NumPy array.
    Applies basic filtering and error handling.
    """
    try:
        # Example: Expecting a string like "1.2,3.4,2.5,..." 
        str_values = lidar_raw.split(',')
        points = np.array([float(val.strip()) for val in str_values if val.strip() != ""])
        logger.info(f"Processed LiDAR data: {points}")
        return points
    except Exception as e:
        logger.error(f"Failed to process LiDAR data: {e}")
        return np.array([])

def detect_obstacles(points, threshold=0.5):
    """
    Simple detection of obstacles based on thresholding.
    Returns list of indices where points exceed threshold.
    """
    try:
        obstacles = [i for i, p in enumerate(points) if p > threshold]
        logger.info(f"Detected obstacles at indices: {obstacles}")
        return obstacles
    except Exception as e:
        logger.error(f"Error detecting obstacles: {e}")
        return []
