import cv2
import json
import os
import time
from typing import Tuple

class GestureCalibrator:
    def __init__(self):
        self.open_hand_threshold = 0.2  # Default
        self.swipe_threshold = 100      # Default (pixels)

    def calibrate(self, get_hand_landmarks, draw_landmarks) -> None:
        """Run calibration for open/closed hand and swipe sensitivity."""
        print("\n=== CALIBRATION MODE ===")
        print("1. Show an OPEN hand (fingers spread) for 3 seconds.")
        print("2. Show a CLOSED hand (fist) for 3 seconds.")
        print("3. Perform a SWIPE (left/right) to set sensitivity.")
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise RuntimeError("Failed to open webcam")

        # Calibrate open/closed hand
        open_values, closed_values = [], []
        print("\nCalibrating hand state...")
        start_time = time.time()
        while time.time() - start_time < 6:  # 6 seconds total
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            results = get_hand_landmarks(frame)
            
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                # Use thumb-tip to index-tip distance as metric
                thumb_tip = hand.landmark[4]
                index_tip = hand.landmark[8]
                distance = ((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)**0.5
                
                if time.time() - start_time < 3:  # First 3s: Open hand
                    open_values.append(distance)
                    cv2.putText(frame, "OPEN HAND", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:  # Next 3s: Closed hand
                    closed_values.append(distance)
                    cv2.putText(frame, "CLOSED HAND", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow("Calibration", frame)
            if cv2.waitKey(1) == ord('q'):
                break

        if open_values and closed_values:
            self.open_hand_threshold = (sum(open_values)/len(open_values) + sum(closed_values)/len(closed_values)) / 2
            print(f"Set open_hand_threshold = {self.open_hand_threshold:.3f}")

        # Calibrate swipe sensitivity
        print("\nCalibrating swipe... Swipe left/right slowly.")
        prev_x = None
        swipe_distances = []
        start_time = time.time()
        while time.time() - start_time < 5:  # 5 seconds
            ret, frame = cap.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            results = get_hand_landmarks(frame)
            
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                index_tip = hand.landmark[8]
                curr_x = index_tip.x * frame.shape[1]
                
                if prev_x is not None:
                    swipe_distances.append(abs(curr_x - prev_x))
                prev_x = curr_x
                cv2.putText(frame, "SWIPE LEFT/RIGHT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            
            cv2.imshow("Calibration", frame)
            if cv2.waitKey(1) == ord('q'):
                break

        if swipe_distances:
            self.swipe_threshold = sum(swipe_distances) / len(swipe_distances)
            print(f"Set swipe_threshold = {self.swipe_threshold:.1f} pixels")

        cap.release()
        cv2.destroyAllWindows()

    def get_thresholds(self) -> Tuple[float, int]:
        """Returns (open_hand_threshold, swipe_threshold)."""
        return self.open_hand_threshold, self.swipe_threshold