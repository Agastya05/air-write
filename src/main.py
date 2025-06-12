import cv2
import numpy as np
from hand_tracking import HandTracker
from painter import Painter
import mediapipe as mp
from collections import deque

# Define color palette and brush sizes
COLOR_PALETTE = [
    ((255, 0, 0), "Blue"),
    ((0, 255, 0), "Green"),
    ((0, 0, 255), "Red"),
    ((0, 255, 255), "Yellow"),
    ((255, 0, 255), "Magenta"),
    ((255, 255, 0), "Cyan"),
    ((128, 0, 128), "Purple"),
    ((0, 128, 255), "Orange"),
    ((128, 128, 128), "Gray"),
    ((0, 0, 0), "Black"),
    ((255, 255, 255), "White"),
]
BRUSH_SIZES = [3, 7, 12, 20, 30]  # Add as many as you like

erase_counter = 0
undo_counter = 0  # Add this near the top of main()

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
    # Draw "Exit" button (bottom left, bigger)
    exit_x1, exit_y1 = 20, h - 90
    exit_x2, exit_y2 = 220, h - 30
    cv2.rectangle(frame, (exit_x1, exit_y1), (exit_x2, exit_y2), (0, 0, 0), -1)
    cv2.putText(frame, "Exit", (exit_x1 + 40, exit_y2 - 15), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3)

    # Draw "Erase All" button next to Exit
    erase_x1, erase_y1 = 240, h - 90
    erase_x2, erase_y2 = 440, h - 30
    cv2.rectangle(frame, (erase_x1, erase_y1), (erase_x2, erase_y2), (0, 0, 255), -1)
    cv2.putText(frame, "Erase All", (erase_x1 + 10, erase_y2 - 15), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)

def main():
    global erase_counter, undo_counter  # Add this line
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
    smooth_points = deque(maxlen=5)  # Keep last 5 points

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        # Optional: Resize for faster processing (uncomment if needed)
        # frame = cv2.resize(frame, (640, 480))

        hand_result = hand_tracker.get_hand_position(frame)

        if hand_result:
            x, y, is_open_palm, confidence, pen_down = hand_result
            if confidence < 0.7:
                painter.stop_drawing()
                draw_ui(frame, selected_color, selected_size)
                output = cv2.addWeighted(frame, 0.5, painter.canvas, 0.5, 0)
                cv2.imshow("Webcam Paint App", output)
                continue
            smooth_points.append((x, y))
            avg_x = int(np.mean([pt[0] for pt in smooth_points]))
            avg_y = int(np.mean([pt[1] for pt in smooth_points]))

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

            h, w, _ = frame.shape  # Make sure this is defined

            # Exit button logic (bottom left, bigger)
            if 20 < avg_x < 220 and (h - 90) < avg_y < (h - 30):
                print("Exit button hovered. Exiting...")
                break

            # Erase All button logic (next to Exit)
            if 240 < avg_x < 440 and (h - 90) < avg_y < (h - 30):
                print("Erase All button hovered. Clearing canvas...")
                painter.clear_canvas()

            # Only draw when pen_down is True
            if pen_down:
                painter.start_drawing()
                # Only draw if movement is significant
                if painter.last_position:
                    dx = avg_x - painter.last_position[0]
                    dy = avg_y - painter.last_position[1]
                    if dx*dx + dy*dy > 4:  # Only draw if moved more than 2 pixels
                        painter.draw_line((avg_x, avg_y))
                else:
                    painter.draw_line((avg_x, avg_y))  # Start drawing at first point
            else:
                painter.stop_drawing()
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

if __name__ == "__main__":
    main()