def draw_circle(image, center, radius, color, thickness=-1):
    cv2.circle(image, center, radius, color, thickness)

def clear_canvas(image, color=(255, 255, 255)):
    image[:] = color

def save_image(image, filename):
    cv2.imwrite(filename, image)