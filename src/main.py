import cv2
import numpy as np
from hand_tracking import HandTracker
from painter import Painter

# Define color palette and brush sizes
COLOR_PALETTE = [
    ((255, 0, 0), "Blue"),
    ((0, 255, 0), "Green"),
    ((0, 0, 255), "Red"),
    ((0, 0, 0), "Black"),
    ((255, 255, 255), "White"),
]
BRUSH_SIZES = [3, 7, 12]

def draw_ui(frame, selected_color, selected_size):
    h, w, _ = frame.shape
    # Draw color palette (top right)
    for i, (color, name) in enumerate(COLOR_PALETTE):
        x1, y1 = w - 60, 10 + i * 50
        x2, y2 = w - 10, 50 + i * 50
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        if color == selected_color:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 200, 200), 3)
    # Draw brush size buttons (top left)
    for i, size in enumerate(BRUSH_SIZES):
        x, y = 20, 20 + i * 60
        cv2.circle(frame, (x, y), size, (200, 200, 200), -1)
        if size == selected_size:
            cv2.circle(frame, (x, y), size + 5, (0, 255, 255), 2)
    # Draw "Erase All" button (top left corner)
    cv2.rectangle(frame, (10, 10), (110, 50), (0, 0, 255), -1)
    cv2.putText(frame, "Erase All", (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

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
    selected_color = COLOR_PALETTE[0][0]
    selected_size = BRUSH_SIZES[0]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Un-mirror the webcam

        # Get hand position and fist status
        hand_result = hand_tracker.get_hand_position(frame)

        if hand_result:
            x, y, _ = hand_result  # Ignore is_fist now

            # Check "Erase All" button
            if 10 < x < 110 and 10 < y < 50:
                painter.clear_canvas()

            # Check color palette
            for i, (color, _) in enumerate(COLOR_PALETTE):
                x1, y1 = frame.shape[1] - 60, 10 + i * 50
                x2, y2 = frame.shape[1] - 10, 50 + i * 50
                if x1 < x < x2 and y1 < y < y2:
                    painter.set_color(color)
                    selected_color = color
            # Check brush size
            for i, size in enumerate(BRUSH_SIZES):
                bx, by = 20, 20 + i * 60
                if (x - bx) ** 2 + (y - by) ** 2 < (size + 10) ** 2:
                    painter.set_brush_size(size)
                    selected_size = size

            painter.set_color(selected_color)
            painter.start_drawing()
            painter.draw_line((x, y))
        else:
            painter.stop_drawing()

        # Draw UI
        draw_ui(frame, selected_color, selected_size)

        # Overlay the canvas on the frame
        output = cv2.addWeighted(frame, 0.5, painter.canvas, 0.5, 0)
        cv2.imshow("Webcam Paint App", output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('c'):
            painter.clear_canvas()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()