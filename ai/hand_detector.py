import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple, List

class HandDetector:
    def __init__(self, max_hands: int = 1, detection_confidence: float = 0.7, tracking_confidence: float = 0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )
        self.landmarks: Optional[List] = None
        self.results = None

    def find_hands(self, frame: np.ndarray, draw: bool = True) -> np.ndarray:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb_frame)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_styles.get_default_hand_landmarks_style(),
                        self.mp_styles.get_default_hand_connections_style(),
                    )
        return frame

    def get_landmarks(self, frame_shape: Tuple[int, int, int]) -> Optional[List[List[float]]]:
        if not self.results or not self.results.multi_hand_landmarks:
            return None

        hand = self.results.multi_hand_landmarks[0]
        h, w, _ = frame_shape
        landmarks = []

        for lm in hand.landmark:
            landmarks.append([lm.x, lm.y, lm.z])

        self.landmarks = landmarks
        return landmarks

    def get_index_finger_tip(self, frame_shape: Tuple[int, int, int]) -> Optional[Tuple[int, int]]:
        landmarks = self.get_landmarks(frame_shape)
        if not landmarks:
            return None

        h, w, _ = frame_shape
        tip = landmarks[8]
        return (int(tip[0] * w), int(tip[1] * h))

    def get_index_finger_normalized(self) -> Optional[Tuple[float, float]]:
        if not self.landmarks:
            return None
        tip = self.landmarks[8]
        return (tip[0], tip[1])

    def release(self):
        self.hands.close()
