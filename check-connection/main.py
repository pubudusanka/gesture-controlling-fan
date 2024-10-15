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

# Function to determine thumb status

# FUNCTION TO CALCULATE ANGLES OF FINGER
def calculate_angle(a, b, c):
    """Calculate the angle (in degrees) between three points (a, b, c)."""
    ba = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]
    
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]
    magnitude_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0

    cosine_angle = dot_product / (magnitude_ba * magnitude_bc)
    # Set the cosine value in range in -1 to 1
    cosine_angle = max(-1, min(1, cosine_angle))
    try:
        angle = math.degrees(math.acos(cosine_angle))
    except ValueError:
        angle = 0
    return angle

# FUNCTION FOR FINDING IF FINGERS ARE CURLED OR NOT
def is_finger_curled(mcp, pip, dip, tip):
    """Determine if a finger is curled based on the angles at its joints."""
    angle_pip = calculate_angle(mcp, pip, dip)
    angle_dip = calculate_angle(pip, dip, tip)
    return angle_pip < 160 or angle_dip < 160
