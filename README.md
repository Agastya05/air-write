# Webcam Paint App 🎨

A real-time interactive painting application that uses your webcam and hand tracking (via MediaPipe) to let you draw, erase, and control brush settings with gestures and on-screen UI.

## Features

- **Draw with your index finger** using hand tracking
- **Color picker**: Select colors by hovering your fingertip over the palette (top right)
- **Brush size selection**: Change brush thickness by hovering over brush size circles (top left)
- **Erase All**: Hover your fingertip over the "Erase All" button (top left) or show an open palm to clear the canvas
- **Smoother drawing**: Interpolated lines for less jitter
- **Performance optimized**: Fast frame processing for real-time interaction

## Requirements

- Python 3.7–3.11 (MediaPipe does **not** support 3.12+)
- [OpenCV](https://pypi.org/project/opencv-python/)
- [MediaPipe](https://pypi.org/project/mediapipe/)
- [NumPy](https://pypi.org/project/numpy/)

Install all dependencies with:

```sh
pip install -r requirements.txt
```

## Usage

1. **Activate your virtual environment** (if using):

   ```sh
   venv\Scripts\activate
   ```

2. **Run the app:**

   ```sh
   python src/main.py
   ```

3. **Controls:**
   - **Draw:** Move your index finger in front of the webcam.
   - **Change color:** Hover your fingertip over a color box (top right).
   - **Change brush size:** Hover over a brush size circle (top left).
   - **Erase All:** Hover over the "Erase All" button (top left) or show an open palm.
   - **Quit:** Press `q`.
   - **Clear canvas (keyboard):** Press `c`.

## Project Structure

```
webcam-paint-app/
├── src/
│   ├── main.py
│   ├── hand_tracking.py
│   ├── painter.py
│   └── ...
├── requirements.txt
└── README.md
```

## Acknowledgements

- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking
- [OpenCV](https://opencv.org/) for image processing

---

Feel free to contribute or suggest new features!
