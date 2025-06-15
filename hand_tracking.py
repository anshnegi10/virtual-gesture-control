import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
import math
import os

# Suppress TensorFlow Lite warnings     
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.85, min_tracking_confidence=0.85)
mp_drawing = mp.solutions.drawing_utils

# Gesture cooldown mechanism
gesture_cooldown = 1.0  # Cooldown time in seconds
last_gesture_time = time.time()

# Keyboard layout
keys = [
    [('Q', (50, 50)), ('W', (110, 50)), ('E', (170, 50)), ('R', (230, 50)), ('T', (290, 50))],
    [('A', (50, 110)), ('S', (110, 110)), ('D', (170, 110)), ('F', (230, 110)), ('G', (290, 110))],
    [('Z', (50, 170)), ('X', (110, 170)), ('C', (170, 170)), ('V', (230, 170)), ('B', (290, 170))],
    [('EMOJI', (50, 230)), ('SPACE', (110, 230)), ('BACK', (230, 230))]
]

# Open Webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Function to check if tap gesture is detected
def is_tap(thumb_pos, index_pos):
    distance = math.dist(thumb_pos, index_pos)
    return distance < 50  # Adjusted sensitivity for tap detection

# Function to process hand landmarks
def get_hand_landmarks(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    return results

# Function to draw hand landmarks
def draw_landmarks(frame, results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            h, w, _ = frame.shape
            landmarks = {id: (int(lm.x * w), int(lm.y * h)) for id, lm in enumerate(hand_landmarks.landmark)}
            return landmarks  # Returns landmark positions of fingers
    return None

# Function to detect gestures
def detect_gestures(landmarks):
    global last_gesture_time

    current_time = time.time()
    thumb_tip = landmarks.get(4, (0, 0))
    index_tip = landmarks.get(8, (0, 0))

    # Detect tap gesture (Thumb & Index close together)
    if current_time - last_gesture_time > gesture_cooldown:
        if is_tap(thumb_tip, index_tip):
            pyautogui.press("space")  # Play/Pause toggle
            print("Gesture: Play/Pause")
            last_gesture_time = current_time

# Main loop to capture video and recognize gestures
try:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Error: Could not capture frame.")
            break

        frame = cv2.flip(frame, 1)
        results = get_hand_landmarks(frame)
        landmarks = draw_landmarks(frame, results)

        # Process gestures only if hand is detected
        if landmarks:
            detect_gestures(landmarks)

        # Display video feed
        cv2.imshow("Gesture Controlled Virtual Keyboard", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
