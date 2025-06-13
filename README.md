# Webcam Paint App 🎨

A real-time interactive painting application that uses your webcam and hand tracking (via MediaPipe) to let you draw, erase, and control brush settings with gestures and on-screen UI.

---

## Features

- **Draw with your index finger** using hand tracking
- **Color picker:** Select colors by hovering your fingertip over the palette (top right)
- **Brush size selection:** Change brush thickness by hovering over brush size circles (top left)
- **Erase All:** Hover your fingertip over the "Erase All" button (bottom left) or press `c` to clear the canvas
- **Exit:** Hover over the "Exit" button (bottom left) or press `q` to quit
- **Expanded color palette:** Choose from a wide range of colors

---

## How to Use

1. **Run the app:**

   ```bash
   python3 src/main.py
   ```

2. **Drawing:**

   - Point your index finger at the camera and move it to draw on the canvas.

3. **Change color:**

   - Hover your fingertip over any color box in the palette (top right).

4. **Change brush size:**

   - Hover your fingertip over any brush size circle (top left).

5. **Erase All:**

   - Hover your fingertip over the "Erase All" button (bottom left), or press `c` on your keyboard.

6. **Exit:**
   - Hover your fingertip over the "Exit" button (bottom left), or press `q` on your keyboard.

---

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- MediaPipe
- NumPy

Install dependencies with:

```bash
pip install opencv-python mediapipe numpy
```

---

## Notes

- Make sure your webcam is connected and not used by another application.
- Grant camera access to your terminal or Python environment in your system settings if needed.
- For best results, use in a well-lit environment.

---

## Credits

- [MediaPipe](https://google.github.io/mediapipe/) for real-time hand tracking
- [OpenCV](https://opencv.org/) for image processing

---

Enjoy painting with your webcam! 🎨🖐️
