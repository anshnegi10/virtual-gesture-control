import pyautogui
import time
import cv2
import math

class GestureDetector:
    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 0.6  # seconds
        self.prev_right_hand_distance = None
        self.prev_left_hand_distance = None

    def distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def execute_action(self, key, text, frame, color=(0, 255, 0), pos=(50, 100)):
        """Press a key and show visual feedback if cooldown passed"""
        if time.time() - self.last_action_time > self.cooldown:
            pyautogui.press(key)
            cv2.putText(frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            self.last_action_time = time.time()

    def detect_gestures(self, handedness, hand_landmarks, frame):
        h, w = frame.shape[:2]

        # Get hand landmark positions (scaled to screen size)
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        wrist = hand_landmarks.landmark[0]
        index_base = hand_landmarks.landmark[5]

        thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
        index_pos = (int(index_tip.x * w), int(index_tip.y * h))
        wrist_pos = (int(wrist.x * w), int(wrist.y * h))
        index_base_pos = (int(index_base.x * w), int(index_base.y * h))

        # Distance between thumb and index tip (zoom gesture)
        thumb_index_distance = self.distance(thumb_pos, index_pos)

        # ------------------ RIGHT HAND (Video Controls) ------------------
        if handedness == "Right":
            if self.prev_right_hand_distance is not None:
                delta = thumb_index_distance - self.prev_right_hand_distance
                if delta > 40:
                    self.execute_action("l", "Next Video →", frame)
                elif delta < -40:
                    self.execute_action("j", "Previous Video ←", frame)
            self.prev_right_hand_distance = thumb_index_distance

            # Tap to play/pause
            if thumb_index_distance < 30:
                self.execute_action("k", "Play / Pause", frame)

        # ------------------ LEFT HAND (Volume Controls) ------------------
        elif handedness == "Left":
            thumb_y = thumb_pos[1]
            wrist_y = wrist_pos[1]
            index_base_y = index_base_pos[1]

            # Like (thumbs up)
            if thumb_y < wrist_y and thumb_y < index_base_y:
                self.execute_action("up", "Volume ↑ (Like)", frame, (0, 255, 255), pos=(50, 160))
            # Dislike (thumbs down)
            elif thumb_y > wrist_y and thumb_y > index_base_y:
                self.execute_action("down", "Volume ↓ (Dislike)", frame, (0, 255, 255), pos=(50, 160))

            # Optional: Zoom for future feature
            self.prev_left_hand_distance = thumb_index_distance
