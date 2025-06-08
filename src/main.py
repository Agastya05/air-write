import cv2
import numpy as np
from hand_tracking import HandTracker
from painter import Painter

def main():
    # Initialize webcam feed
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read from webcam.")
        return

    canvas = np.zeros_like(frame)
    hand_tracker = HandTracker()
    painter = Painter(canvas)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Un-mirror the webcam

        # Get hand position
        hand_position = hand_tracker.get_hand_position(frame)

        # If hand is detected, update painter
        if hand_position:
            painter.start_drawing()
            painter.draw_line(hand_position)
        else:
            painter.stop_drawing()

        # Overlay the canvas on the frame
        output = cv2.addWeighted(frame, 0.5, painter.canvas, 0.5, 0)
        cv2.imshow("Webcam Paint App", output)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()