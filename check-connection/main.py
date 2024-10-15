import cv2
import mediapipe as mp
import serial
import time
import math
import numpy as np
import os

cap = cv2.VideoCapture(0)
speed = 155
onSpeed = 155
pTime = 0
cTime = 0

# Initialize MediaPipe hand detection
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

try:
    arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1, write_timeout=2)
    time.sleep(2)  # Wait for the serial connection to initialize
    arduino_connected = True

    # Send data to Arduino
    arduino.write(b'1')  # Send '1' to the Arduino
    print("=========================================")
    print("Sent request to arduino")
    # Wait a moment for the Arduino to respond
    time.sleep(1)

    # Read response from Arduino
    response = arduino.readline().decode('utf-8').strip()  # Read and decode response
    if response:
        print("Arduino response to the request")
    else:
        print("No response from Arduino")

except serial.serialutil.SerialException as e:
    print(f"Error Connecting to Arduino: {e}")
    arduino_connected = False

print("Arduino connection is : ", arduino_connected)
print("=========================================")