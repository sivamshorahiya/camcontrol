# CAM CONTROL

This project uses a webcam to track your nose and hand movements to control the mouse cursor and perform clicks. It leverages computer vision and machine learning libraries like OpenCV and MediaPipe, and automation tools like PyAutoGUI.

## Features
- Control the mouse cursor using the position of your nose.
- Perform single and double clicks based on nose and hand gestures.
- Retrieve and print information about the window under the cursor.
- Automatically decides whether to single click or double click depending on file types, element, or component type if the mouse pointer waits for 3-4 seconds.

## Installation

### Requirements

To install the necessary packages, you need to have Python installed. You can install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

### requirements.txt

```bash
opencv-python-headless
mediapipe
pyautogui
pygetwindow
pywinauto
pypiwin32
```

### Running the Application

1. Ensure your webcam is connected and properly configured.
2. Run the script:

```bash
python main.py
```

## Notes
- Make sure to run the script in an environment where you have access to a webcam.
- The code is configured to run on Windows due to dependencies on `pywinauto` and `pygetwindow`.

## License
This project is licensed under the MIT License.
