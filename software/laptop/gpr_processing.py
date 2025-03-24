"""
laptop/gpr_processing.py
Processes raw GPR sensor data and extracts potential anomalies.
"""
import numpy as np
import logging
from scipy.signal import butter, filtfilt

logger = logging.getLogger("GprProcessing")
logger.setLevel(logging.INFO)

def process_gpr_data(gpr_raw):
    """
    Convert raw GPR data (comma-separated values) to NumPy array and apply filtering.
    """
    try:
        str_values = gpr_raw.split(',')
        data = np.array([float(val.strip()) for val in str_values if val.strip() != ""])
        filtered = butter_bandpass_filter(data, lowcut=100, highcut=1000, fs=4000, order=3)
        logger.info("GPR data processed and filtered")
        return filtered
    except Exception as e:
        logger.error(f"Failed to process GPR data: {e}")
        return np.array([])

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Apply a Butterworth bandpass filter.
    """
    try:
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        filtered_data = filtfilt(b, a, data)
        return filtered_data
    except Exception as e:
        logger.error(f"Error in bandpass filter: {e}")
        return data

def detect_anomalies(data, threshold=0.8):
    """
    Detect anomalies in the filtered GPR data.
    Returns indices where data exceeds the threshold.
    """
    try:
        anomalies = [i for i, val in enumerate(data) if val > threshold]
        logger.info(f"Detected anomalies at indices: {anomalies}")
        return anomalies
    except Exception as e:
        logger.error(f"Error detecting anomalies: {e}")
        return []
