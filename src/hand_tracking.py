import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

    def get_hand_position(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        if results.multi_hand_landmarks and results.multi_handedness:
            hand_landmarks = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0].classification[0].label
            confidence = results.multi_handedness[0].classification[0].score

            # Index finger tip
            x = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x * frame.shape[1])
            y = int(hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * frame.shape[0])

            # Strict open palm detection: all finger tips well above their MCP joints
            threshold = 0.04  # You can tune this value for your hand/camera

            tips = [
                self.mp_hands.HandLandmark.THUMB_TIP,
                self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
                self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                self.mp_hands.HandLandmark.RING_FINGER_TIP,
                self.mp_hands.HandLandmark.PINKY_TIP
            ]
            mcps = [
                self.mp_hands.HandLandmark.THUMB_MCP,
                self.mp_hands.HandLandmark.INDEX_FINGER_MCP,
                self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                self.mp_hands.HandLandmark.RING_FINGER_MCP,
                self.mp_hands.HandLandmark.PINKY_MCP
            ]
            is_open_palm = all(
                hand_landmarks.landmark[tip].y < hand_landmarks.landmark[mcp].y - threshold
                for tip, mcp in zip(tips, mcps)
            )

            # Define landmarks for pen_down logic
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]
            pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
            pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]

            # Pen down: index finger up, others down, with threshold
            threshold = 0.035 # You can try 0.02 or 0.025 if still not detected
            pen_down = (
                (index_tip.y < index_mcp.y - threshold) and
                (middle_tip.y > middle_mcp.y - threshold) and
                (ring_tip.y > ring_mcp.y - threshold) and
                (pinky_tip.y > pinky_mcp.y - threshold)
            )

            return x, y, is_open_palm, confidence, pen_down
        return None
