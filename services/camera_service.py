import cv2
import numpy as np
import base64
import time
from typing import Optional, Tuple
from ai.hand_detector import HandDetector
from ai.gesture_classifier import GestureClassifier
from app.models.game import Gesture

class CameraService:
    def __init__(self):
        self.cap: Optional[cv2.VideoCapture] = None
        self.detector = HandDetector(max_hands=1)
        self.classifier = GestureClassifier()
        self.fps = 0
        self.frame_count = 0
        self.last_fps_time = time.time()
        self.is_running = False

    def start(self, camera_index: int = 0) -> bool:
        try:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                return False
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.is_running = True
            return True
        except Exception:
            return False

    def stop(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.detector.release()

    def get_frame(self) -> Optional[np.ndarray]:
        if not self.cap or not self.is_running:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv2.flip(frame, 1)

    def process_frame(self, frame: np.ndarray) -> dict:
        self._update_fps()
        processed = self.detector.find_hands(frame, draw=True)
        landmarks = self.detector.get_landmarks(processed.shape)
        
        gesture = Gesture.NONE
        cursor_x, cursor_y = 0.0, 0.0
        confidence = 0.0

        if landmarks:
            gesture_raw = self.classifier.classify(landmarks)
            gesture = self.classifier.smooth_gesture(gesture_raw)
            index_pos = self.detector.get_index_finger_normalized()
            if index_pos:
                cursor_x, cursor_y = index_pos
                confidence = 0.9

        try:
            success, buffer = cv2.imencode('.jpg', processed, [cv2.IMWRITE_JPEG_QUALITY, 70])
            if not success:
                raise ValueError("Failed to encode frame")
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
        except Exception:
            frame_base64 = ""

        return {
            "frame": frame_base64,
            "gesture": gesture.value,
            "cursor_x": cursor_x,
            "cursor_y": cursor_y,
            "confidence": confidence,
            "fps": self.fps,
            "landmarks": landmarks,
        }

    def _update_fps(self):
        self.frame_count += 1
        now = time.time()
        if now - self.last_fps_time >= 1.0:
            self.fps = self.frame_count
            self.frame_count = 0
            self.last_fps_time = now
