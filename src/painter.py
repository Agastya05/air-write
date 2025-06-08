import cv2

class Painter:
    def __init__(self, canvas):
        self.canvas = canvas
        self.drawing = False
        self.last_position = None

    def start_drawing(self):
        self.drawing = True

    def stop_drawing(self):
        self.drawing = False
        self.last_position = None

    def draw_line(self, current_position):
        if self.drawing and self.last_position is not None:
            cv2.line(self.canvas, self.last_position, current_position, (255, 0, 0), 5)
        self.last_position = current_position

    def clear_canvas(self):
        self.canvas.fill(255)  # Assuming a white canvas

    def save_image(self, filename):
        cv2.imwrite(filename, self.canvas)