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

#Function to Turn-On
def turn_on(handLms, img_shape):
    h, w, c = img_shape
    
    thumb_tip = handLms.landmark[4]
    thumb_pip = handLms.landmark[3]
    index_finger_tip = handLms.landmark[8]
    index_finger_dip = handLms.landmark[7]
    middle_finger_tip = handLms.landmark[12]
    middle_finger_mcp = handLms.landmark[9]
    ring_finger_tip = handLms.landmark[16]
    ring_finger_mcp = handLms.landmark[13]
    pinky_tip = handLms.landmark[20]
    pinky_dip = handLms.landmark[19]

    thumb_tip_y = int(thumb_tip.y * h)
    thumb_pip_y = int(thumb_pip.y * h)
    index_finger_tip_y = int(index_finger_tip.y * h)
    index_finger_dip_y = int(index_finger_dip.y * h)
    middle_finger_tip_y = int(middle_finger_tip.y * h)
    middle_finger_mcp_y = int(middle_finger_mcp.y * h)
    ring_finger_tip_y = int(ring_finger_tip.y * h)
    ring_finger_mcp_y = int(ring_finger_mcp.y * h)
    pinky_tip_y = int(pinky_tip.y * h)
    pinky_dip_y = int(pinky_dip.y * h)

    # Get the coordinates of the finger joints in pixel space
    fingers = {
        'middle': [handLms.landmark[i] for i in [9, 10, 11, 12]],
        'ring': [handLms.landmark[i] for i in [13, 14, 15, 16]],
    }

    all_fingers_curled = True
    for finger_name, landmarks in fingers.items():
        mcp = (int(landmarks[0].x * w), int(landmarks[0].y * h))
        pip = (int(landmarks[1].x * w), int(landmarks[1].y * h))
        dip = (int(landmarks[2].x * w), int(landmarks[2].y * h))
        tip = (int(landmarks[3].x * w), int(landmarks[3].y * h))
        
        if not is_finger_curled(mcp, pip, dip, tip):
            all_fingers_curled = False
            break
        
    if all_fingers_curled and (index_finger_dip_y > index_finger_tip_y) and (pinky_dip_y > pinky_tip_y) :
        return True
    return False

#Function to Turn-off
def turn_off(handLms, img_shape):
    h, w, c = img_shape
    
    thumb_tip = handLms.landmark[4]
    thumb_pip = handLms.landmark[3]
    index_finger_tip = handLms.landmark[8]
    index_finger_dip = handLms.landmark[7]
    middle_finger_tip = handLms.landmark[12]
    middle_finger_dip = handLms.landmark[11]
    ring_finger_tip = handLms.landmark[16]
    ring_finger_dip = handLms.landmark[15]
    pinky_tip = handLms.landmark[20]
    pinky_dip = handLms.landmark[19]

    thumb_tip_y = int(thumb_tip.y * h)
    thumb_pip_y = int(thumb_pip.y * h)
    index_finger_tip_y = int(index_finger_tip.y * h)
    index_finger_dip_y = int(index_finger_dip.y * h)
    middle_finger_tip_y = int(middle_finger_tip.y * h)
    middle_finger_dip_y = int(middle_finger_dip.y * h)
    ring_finger_tip_y = int(ring_finger_tip.y * h)
    ring_finger_dip_y = int(ring_finger_dip.y * h)
    pinky_tip_y = int(pinky_tip.y * h)
    pinky_dip_y = int(pinky_dip.y * h)

    # Ensure all fingers (except thumb) are curled
    fingers = {
        'thumb': [handLms.landmark[i] for i in [1, 2, 3, 4]],
        'index': [handLms.landmark[i] for i in [5, 6, 7, 8]],
        'middle': [handLms.landmark[i] for i in [9, 10, 11, 12]],
        'ring': [handLms.landmark[i] for i in [13, 14, 15, 16]],
        'pinky': [handLms.landmark[i] for i in [17, 18, 19, 20]],
    }

    all_fingers_curled = False
    for finger_name, landmarks in fingers.items():
        mcp = (int(landmarks[0].x * w), int(landmarks[0].y * h))
        pip = (int(landmarks[1].x * w), int(landmarks[1].y * h))
        dip = (int(landmarks[2].x * w), int(landmarks[2].y * h))
        tip = (int(landmarks[3].x * w), int(landmarks[3].y * h))
        
        if not is_finger_curled(mcp, pip, dip, tip):
            all_fingers_curled = True
            break

    if all_fingers_curled and (thumb_tip_y < thumb_pip_y) and (index_finger_tip_y < index_finger_dip_y) and (middle_finger_tip_y < middle_finger_dip_y) and (ring_finger_tip_y < ring_finger_dip_y) and (pinky_tip_y < pinky_dip_y):
        return True
    return False
