# Drone-Based Landslide Search and Rescue System

## Project Overview
This project develops a drone-based system equipped with LiDAR, Ground Penetrating Radar (GPR), and other sensors to assist in locating individuals trapped in landslides. The system processes sensor data in real time, performs analysis on a laptop, and sends control commands back to a Raspberry Pi (RPI) for autonomous drone navigation.

## Architecture
- **Raspberry Pi (rpi/):**  
  - Reads sensor data from LiDAR and GPR using serial interfaces.
  - Publishes sensor data to the laptop via MQTT.
  - Listens for drone control commands via MQTT.
  - Controls drone movement via MAVLink commands.
  
- **Laptop (laptop/):**  
  - Receives sensor data from the Raspberry Pi.
  - Processes LiDAR and GPR data (e.g., anomaly detection, obstacle identification).
  - Decides on drone actions and sends commands back via MQTT.
  
- **Shared (shared/):**  
  - Contains utilities and message protocols for consistent communication and data handling.

## Setup Instructions
1. **Hardware Setup:**  
   - Connect LiDAR and GPR sensors to the Raspberry Pi.
   - Ensure the drone flight controller is connected and accessible via MAVLink.
  
2. **Software Installation:**
   - For the Raspberry Pi, install dependencies listed in `rpi/requirements.txt`:
     ```
     pip install -r rpi/requirements.txt
     ```
   - For the Laptop, install dependencies listed in `laptop/requirements.txt`:
     ```
     pip install -r laptop/requirements.txt
     ```

3. **Configuration:**  
   - Update IP addresses, serial ports, and other parameters in `rpi/config.py` and `laptop/config.py` as needed.

4. **Running the System:**  
   - Start the Raspberry Pi main script:
     ```
     python rpi/main.py
     ```
   - Start the Laptop main processing script:
     ```
     python laptop/main.py
     ```

## Debugging & Simulation
- **MQTT Testing:** Use Mosquitto clients to verify message flows.
- **Sensor Testing:** Run individual scripts (e.g., testing LiDAR and GPR interfaces) to verify sensor outputs.
- **Simulation:** Integrate Gazebo or AirSim for simulated drone testing.

## Future Enhancements
- Integration of computer vision (using OpenCV) for enhanced object detection.
- Advanced machine learning algorithms for improved anomaly detection.
- Deployment of thermal cameras for night operations.

## Project Overview

```
software/
├── rpi/
│   ├── main.py                # Main script to collect sensor data and send to laptop
│   ├── lidar.py               # LiDAR sensor interface
│   ├── gpr.py                 # GPR sensor interface
│   ├── drone_control.py       # Drone movement and motor control
│   ├── config.py              # Configuration settings (IP, ports, sensor calibration)
│   ├── requirements.txt       # Python dependencies for RPi
│
├── laptop/
│   ├── main.py                # Main processing loop: subscribes, processes, commands
│   ├── receiver.py            # Handles incoming data from RPi
│   ├── lidar_processing.py    # LiDAR data processing and object detection
│   ├── gpr_processing.py      # GPR data processing and anomaly detection
│   ├── drone_commands.py      # Sends control commands back to RPi
│   ├── config.py              # Configuration settings for networking
│   ├── requirements.txt       # Python dependencies for Laptop
│
└── shared/
    ├── utils.py               # Shared utilities like logging and transformations
    ├── message_protocol.py    # Defines message formats for communication
    
└── README.md
