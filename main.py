import cv2
import mediapipe as mp
import pyautogui
import time
import win32gui
import pywintypes
import pygetwindow as gw
from pywinauto import Desktop, Application

# Setup
cam = cv2.VideoCapture(0)
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
screen_w, screen_h = pyautogui.size()
sensitivity = 25.0
smoothing_factor = 0.15

# Move cursor to the center initially
pyautogui.moveTo(screen_w // 2, screen_h // 2)

initial_x = None
initial_y = None
smoothed_x = None
smoothed_y = None

last_x, last_y = None, None
last_time = None
hover_threshold = 3.5

def get_window_info(x, y):
    try:
        desktop = Desktop(backend="uia")
        element = desktop.from_point(x, y)
        element2 = desktop.top_from_point(x, y)
        
        window_title = element.window_text()
        window_class = element.class_name()
        name = element2.window_text()
        type = element2.class_name()
        print(Desktop.windows)
        
        
        if window_title == "Settings" and window_class == "ApplicationFrameWindow":
            print("Got file")
        elif window_class.endswith("FolderView") or window_class == "CabinetWClass":
            print("Got directory")
        elif window_class.endswith("ApplicationFrameWindow"):
            print("Got application")
        elif window_class.endswith("UI"):
            print("Got UI element")
        
        return window_class, window_title, name, type
    except Exception as e:
        print(f"Error: {e}")
        return "Unknown", "Unknown", "Unknown", "Unknown"
    

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_output = face_mesh.process(rgb_frame)
    face_landmark_points = face_output.multi_face_landmarks

    hand_output = hands.process(rgb_frame)
    hand_landmarks = hand_output.multi_hand_landmarks

    frame_h, frame_w, _ = frame.shape

    if face_landmark_points:
        face_landmarks = face_landmark_points[0].landmark

        nose_tip = face_landmarks[1]

        x = int(nose_tip.x * frame_w)
        y = int(nose_tip.y * frame_h)
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        if initial_x is None and initial_y is None:
            initial_x = nose_tip.x
            initial_y = nose_tip.y
            smoothed_x = initial_x
            smoothed_y = initial_y

        delta_x = (nose_tip.x - initial_x) * sensitivity
        delta_y = (nose_tip.y - initial_y) * sensitivity

        smoothed_x = (1 - smoothing_factor) * smoothed_x + smoothing_factor * delta_x
        smoothed_y = (1 - smoothing_factor) * smoothed_y + smoothing_factor * delta_y

        screen_x = screen_w // 2 + (screen_w * smoothed_x)
        screen_y = screen_h // 2 + (screen_h * smoothed_y)

        pyautogui.moveTo(screen_x, screen_y)

        # Get information about window under the cursor
        try:
            ClassName, Name, Title, ClassType = get_window_info(int(screen_x), int(screen_y))
            print(f"\n\n\n\n\nName: {Name}, ClassName: {ClassName} \n Title: {Title}, ClassType: {ClassType}")
        except pywintypes.error:
            print("Unable to retrieve window information.")

        # Determine whether to single or double click
        if ClassName == ClassType:
            print("Detected free space region.\n\n\n\n")
        elif Name != "" and ClassType == "SysListView32" or ClassName == "UIProperty":
            print("Detected file explorer region.\n\n\n\n")
            if last_x is not None and last_y is not None:
                if abs(screen_x - last_x) < 20 and abs(screen_y - last_y) < 20:
                    if last_time is None:
                        last_time = time.time()
                    elif time.time() - last_time > 3:
                        print("Performing double click.")
                        pyautogui.doubleClick()
                        last_time = None
                else:
                    last_time = time.time()
        elif ClassType == "Shell_TrayWnd":
            print("Detected taskbar region.\n\n\n\n")
            if last_x is not None and last_y is not None:
                if abs(screen_x - last_x) < 20 and abs(screen_y - last_y) < 20:
                    if last_time is None:
                        last_time = time.time()
                    elif time.time() - last_time > 3:
                        print("Performing single click.")
                        pyautogui.click()
                        last_time = None
                else:
                    last_time = time.time()

        else:
            print("Detected unknown region.\n\n\n\n")
            if last_x is not None and last_y is not None:
                if abs(screen_x - last_x) < 20 and abs(screen_y - last_y) < 20:
                    if last_time is None:
                        last_time = time.time()
                    elif time.time() - last_time > hover_threshold:
                        print("Performing single click.")
                        pyautogui.click()
                        last_time = None
                else:
                    last_time = time.time()
        last_x, last_y = screen_x, screen_y

    # Check for index finger presence to trigger double click
    if hand_landmarks:
        for hand_landmark in hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)
            index_finger_tip = hand_landmark.landmark[8]
            if index_finger_tip:
                print("Detected hand index finger for double click.")
                pyautogui.doubleClick()
                pyautogui.sleep(1)

    cv2.imshow('Nose Controlled Mouse and Hand Double Click', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()