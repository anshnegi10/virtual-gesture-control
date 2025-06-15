from charset_normalizer import detect
import cv2
import time
import pyautogui
import numpy as np
import sys
import os
import json

# Add virtual_keyboard directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'virtual_keyboard')))

from hand_tracking import get_hand_landmarks, draw_landmarks, cleanup
from Utils.gesture_detection import GestureDetector
from Utils.calibration import GestureCalibrator


print("[INFO] Starting Virtual Keyboard...")
detect.mode = "media"

# -------- Load or Run Calibration -------- #
calibration_file = "calibration.json"
if os.path.exists(calibration_file):
    with open(calibration_file, 'r') as f:
        data = json.load(f)
        open_hand_threshold = data.get("open_hand_threshold", 0.2)
        swipe_threshold = data.get("swipe_threshold", 100)
    print(f"[INFO] Calibration loaded: Open Threshold={open_hand_threshold}, Swipe Threshold={swipe_threshold}")
else:
    calibrator = GestureCalibrator()
    calibrator.calibrate(get_hand_landmarks, draw_landmarks)
    open_hand_threshold, swipe_threshold = calibrator.get_thresholds()
    with open(calibration_file, 'w') as f:
        json.dump({"open_hand_threshold": open_hand_threshold, "swipe_threshold": swipe_threshold}, f)
    print(f"[INFO] Calibration saved: Open Threshold={open_hand_threshold}, Swipe Threshold={swipe_threshold}")

# -------- Webcam Initialization -------- #
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[ERROR] Could not open webcam")
    sys.exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 20)
print("[INFO] Webcam initialized successfully")

# -------- Keyboard Layout -------- #
keys = (
    [  # QWERTY Layout
        [('Q', (50, 50)), ('W', (110, 50)), ('E', (170, 50)), ('R', (230, 50)), ('T', (290, 50))],
        [('A', (50, 110)), ('S', (110, 110)), ('D', (170, 110)), ('F', (230, 110)), ('G', (290, 110))],
        [('Z', (50, 170)), ('X', (110, 170)), ('C', (170, 170)), ('V', (230, 170)), ('B', (290, 170))],
        [('EMOJI', (50, 230)), ('SPACE', (110, 230)), ('BACK', (230, 230))]
    ],
    [  # Emoji Layout
        [('😊', (50, 50)), ('😂', (110, 50)), ('😍', (170, 50))],
        [('👍', (50, 110)), ('👎', (110, 110)), ('🙌', (170, 110))]
    ]
)

# -------- Gesture Detector Initialization -------- #
detector = GestureDetector()
detector.open_hand_threshold = open_hand_threshold
detector.swipe_threshold = swipe_threshold
is_emoji_mode = False
print("[INFO] Gesture detector initialized")

# -------- Minimize this window to focus app -------- #
cv2.namedWindow('Virtual Keyboard')
cv2.imshow('Virtual Keyboard', np.zeros((480, 640, 3), dtype=np.uint8))
pyautogui.hotkey('alt', 'space')
pyautogui.press('n')  # Minimize window

# -------- Indicator for Mode Switch -------- #
last_mode = detector.mode
mode_toggle_time = 0
MODE_INDICATOR_DURATION = 1.0  # in seconds

try:
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame")
            break

        frame = cv2.flip(frame, 1)
        results = get_hand_landmarks(frame)

        if results.multi_hand_landmarks:
            print(f"[INFO] Hands detected: {len(results.multi_hand_landmarks)}")

        # Draw keyboard layout
        if detector.mode == "keyboard":
            layout = keys[1] if is_emoji_mode else keys[0]
            for row in layout:
                for key, (x, y) in row:
                    cv2.rectangle(frame, (x, y), (x + 50, y + 50), (0, 255, 0), 2)
                    cv2.putText(frame, key, (x + 10, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Draw gesture cheat sheet (for media control)
        elif detector.mode == "media":
            y = 90
            instructions = [
                ("Right Hand Gestures:", (255, 255, 0)),
                ("- Open Hand: Play/Pause", (0, 0, 255)),
                ("- Double Open: Full Screen", (0, 0, 255)),
                ("- Swipe Right: Next Video", (0, 0, 255)),
                ("- Swipe Left: Previous Video", (0, 0, 255)),
                ("- Swipe Up: Seek Forward", (0, 0, 255)),
                ("- Swipe Down: Seek Backward", (0, 0, 255)),
                ("Left Hand Gestures:", (255, 255, 0)),
                ("- Open Hand: Mute/Unmute", (255, 0, 0)),
                ("- Swipe Up: Volume Up", (255, 0, 0)),
                ("- Double Swipe Up: Toggle Window", (255, 0, 0)),
                ("- Swipe Down: Volume Down", (255, 0, 0)),
            ]
            for text, color in instructions:
                cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                y += 30

        # -------- Gesture Detection -------- #
        for handedness, hand_landmarks, index_pos in draw_landmarks(frame, results):
            print(f"[INFO] {handedness} hand at {index_pos}")
            action = detector.detect_gestures(handedness, hand_landmarks, index_pos, frame, keys, is_emoji_mode)
            if action == "toggle_emoji":
                is_emoji_mode = not is_emoji_mode

        # -------- Mode Switch Feedback -------- #
        if detector.mode != last_mode:
            mode_toggle_time = time.time()
            last_mode = detector.mode
        if time.time() - mode_toggle_time < MODE_INDICATOR_DURATION:
            color = (0, 255, 0) if detector.mode == "keyboard" else (255, 0, 0)
            cv2.rectangle(frame, (10, 70), (110, 100), color, -1)
            cv2.putText(frame, f"Mode: {detector.mode}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # -------- FPS Display -------- #
        fps = 1 / max((time.time() - start_time), 1e-5)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Mode: {detector.mode}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # -------- Show Frame -------- #
        cv2.imshow('Virtual Keyboard', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('c'):
            print("[INFO] Recalibrating...")
            calibrator = GestureCalibrator()
            calibrator.calibrate(get_hand_landmarks, draw_landmarks)
            detector.open_hand_threshold, detector.swipe_threshold = calibrator.get_thresholds()
            with open(calibration_file, 'w') as f:
                json.dump({
                    "open_hand_threshold": detector.open_hand_threshold,
                    "swipe_threshold": detector.swipe_threshold
                }, f)
            print(f"[INFO] Reca      librated: Open Threshold={detector.open_hand_threshold}, Swipe Threshold={detector.swipe_threshold}")

except KeyboardInterrupt:
    print("\n[INFO] Stopped by user")
except Exception as e:
    print(f"[ERROR] Exception occurred: {e}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    cleanup()
    print("[INFO] Cleanup completed successfully")
    