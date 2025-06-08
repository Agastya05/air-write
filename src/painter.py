import cv2

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
            cv2.line(self.canvas, self.last_position, current_position, self.color, self.brush_size)
        self.last_position = current_position

    def clear_canvas(self):
        self.canvas.fill(0)  # Black canvas