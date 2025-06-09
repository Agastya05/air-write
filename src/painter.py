import cv2
import numpy as np

class Painter:
    def __init__(self, canvas):
        self.canvas = canvas
        self.drawing = False
        self.last_position = None
        self.color = (255, 0, 0)  # Default: Blue
        self.brush_size = 5

    def set_color(self, color):
        self.color = color

    def set_brush_size(self, size):
        self.brush_size = size

    def start_drawing(self):
        self.drawing = True

    def stop_drawing(self):
        self.drawing = False
        self.last_position = None

    def draw_line(self, current_position):
        if self.drawing and self.last_position is not None:
            # Interpolate points between last_position and current_position
            x1, y1 = self.last_position
            x2, y2 = current_position
            dist = int(np.hypot(x2 - x1, y2 - y1))
            for i in range(1, dist + 1):
                t = i / dist
                x = int(x1 + (x2 - x1) * t)
                y = int(y1 + (y2 - y1) * t)
                cv2.circle(self.canvas, (x, y), self.brush_size // 2, self.color, -1)
        self.last_position = current_position

    def clear_canvas(self):
        self.canvas.fill(0)