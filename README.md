# Hand Gesture Controlled Fan using Python and Arduino

This project uses hand gestures to control the speed and power of a fan motor. The hand gestures are detected using Python's OpenCV and Mediapipe libraries, while an Arduino controls the fan motor speed based on the detected gestures. 

## Table of Contents
- [Overview](#overview)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)


## Overview

The project detects different hand gestures via a webcam and uses the detected signals to control a fan motor connected to an Arduino board. The gestures include:
- **🤟**: Fan ON at max speed
- **🤚**: Fan OFF
- **👎**: Fan speed decrease
- **👍**: Fan speed increase

## Hardware Requirements

- Arduino Uno
- A4988 Motor Driver
- DC Motor
- Webcam
- Breadboard and Jumper Wires
- Power Supply for the Motor
- Hand Gesture Recognition (via webcam)

## Software Requirements

- [Python 3.x](https://www.python.org/)
- [OpenCV](https://opencv.org/) for image processing
- [Mediapipe](https://mediapipe.dev/) for hand gesture detection
- [Arduino IDE](https://www.arduino.cc/en/software) for uploading code to the Arduino
- [PySerial](https://pythonhosted.org/pyserial/) for serial communication between Python and Arduino

## Features

- Detects hand gestures using a webcam
- Sends commands to an Arduino to control the fan motor
- Controls fan speed based on different hand gestures
- Fan can be turned on/off and adjusted to different speeds

## How It Works

1. **Gesture Detection**: 
   The Python script uses Mediapipe to detect hand gestures via the webcam. Each hand gesture corresponds to a specific fan control command (on, off, speed up, slow down).

2. **Arduino Communication**: 
   The Python script sends the command to the Arduino via serial communication. The Arduino receives these commands and adjusts the motor's speed or power accordingly.

3. **Motor Control**: 
   The Arduino controls the motor driver (A4988) to set the motor's speed. Depending on the gesture, the fan will either turn on, turn off, or adjust to a different speed.

## Installation

1. **Python Setup**:
    - Install Python 3.x from [python.org](https://www.python.org/)
    - Install the required Python packages:
      ```bash
      pip install opencv-python mediapipe pyserial
      ```

2. **Arduino Setup**:
    - Install the Arduino IDE from [arduino.cc](https://www.arduino.cc/en/software)
    - Upload the Arduino code provided below to your Arduino Uno.

## Usage

1. Run the Python script for hand gesture detection:
    ```bash
    python hand_gesture_control.py
    ```

2. Ensure that the Arduino is connected to the correct COM port.

3. Use the following gestures to control the fan:
    - **🤟**: Fan ON at max speed
    - **🤚**: Fan OFF
    - **👎**: Fan speed decrease
    - **👍**: Fan speed increase


