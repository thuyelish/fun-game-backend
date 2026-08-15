import numpy as np
from typing import Optional, List, Tuple
from app.models.game import Gesture

class GestureClassifier:
    def __init__(self):
        self.PINCH_THRESHOLD = 0.06
        self.last_gesture = Gesture.NONE
        self.gesture_history: List[Gesture] = []
        self.history_size = 5

    def _finger_is_up(self, landmarks: List[List[float]], finger_tip: int, finger_pip: int) -> bool:
        return landmarks[finger_tip][1] < landmarks[finger_pip][1]

    def _thumb_is_up(self, landmarks: List[List[float]]) -> bool:
        return landmarks[4][0] < landmarks[3][0]

    def _is_pinch(self, landmarks: List[List[float]]) -> bool:
        thumb_tip = np.array(landmarks[4][:2])
        index_tip = np.array(landmarks[8][:2])
        distance = np.linalg.norm(thumb_tip - index_tip)
        return distance < self.PINCH_THRESHOLD

    def classify(self, landmarks: List[List[float]]) -> Gesture:
        if not landmarks or len(landmarks) < 21:
            return Gesture.NONE

        if self._is_pinch(landmarks):
            return Gesture.PINCH

        thumb_up = self._thumb_is_up(landmarks)
        index_up = self._finger_is_up(landmarks, 8, 6)
        middle_up = self._finger_is_up(landmarks, 12, 10)
        ring_up = self._finger_is_up(landmarks, 16, 14)
        pinky_up = self._finger_is_up(landmarks, 20, 18)

        fingers_up = sum([thumb_up, index_up, middle_up, ring_up, pinky_up])

        if fingers_up == 5:
            return Gesture.FIVE_FINGERS

        if fingers_up == 0:
            return Gesture.CLOSED_FIST

        if index_up and not middle_up and not ring_up and not pinky_up:
            return Gesture.INDEX_FINGER

        if index_up and middle_up and not ring_up and not pinky_up:
            return Gesture.VICTORY

        if fingers_up >= 4:
            return Gesture.OPEN_PALM

        return Gesture.NONE

    def smooth_gesture(self, gesture: Gesture) -> Gesture:
        self.gesture_history.append(gesture)
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)

        if len(self.gesture_history) >= 3:
            recent = self.gesture_history[-3:]
            if recent[0] == recent[1] == recent[2]:
                self.last_gesture = recent[0]
                return recent[0]

        return self.last_gesture

    def reset(self):
        self.last_gesture = Gesture.NONE
        self.gesture_history.clear()
