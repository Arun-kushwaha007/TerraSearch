"""
shared/utils.py
Shared utilities for data transformation and logging.
"""
import logging
import numpy as np

logger = logging.getLogger("SharedUtils")
logger.setLevel(logging.INFO)

def normalize_data(data):
    """
    Normalize a NumPy array to the range [0, 1].
    """
    try:
        data_min = np.min(data)
        data_max = np.max(data)
        if data_max - data_min == 0:
            logger.warning("Data has zero variation; returning zeros")
            return np.zeros_like(data)
        normalized = (data - data_min) / (data_max - data_min)
        return normalized
    except Exception as e:
        logger.error(f"Error normalizing data: {e}")
        return data
