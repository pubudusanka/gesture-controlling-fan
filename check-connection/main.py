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
