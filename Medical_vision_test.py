# Copyright (c) 2025 aiMahdiX
# This file is part of the Ophthalmology Vision Test System


import cv2
import numpy as np
import mediapipe as mp
import pygame
import random
import time
import math
import warnings
import os
import tkinter as tk
from tkinter import filedialog
from google import genai
from google.genai import types
import pygame_gui
from pygame_gui.elements import UIButton, UITextEntryLine
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from collections import Counter
from datetime import datetime
import logging
import threading
import matplotlib.pyplot as plt  # For generating medical charts
import json  # add this import near the top

GEMINI_API_KEY = ""  # add default value for GEMINI_API_KEY
screen_diag_in = None
mm_per_pixel = None

# ------------------------------
# Initial Setup
# ------------------------------
pygame.init()
logging.basicConfig(level=logging.INFO)
logging.getLogger('mediapipe').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ------------------------------
# Loading Background Images and Loading Screen
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to Optotype font file
OPTOTYPE_FONT_PATH = os.path.join(BASE_DIR, "assets", "fonts", "Snellen.ttf")

def get_optotype_font(size_px):
    """
    Returns a pygame.font.Font from the Snellen font with size_px pixels
    """
    return pygame.font.Font(OPTOTYPE_FONT_PATH, size_px)

save_folder = os.path.join(BASE_DIR, "results")
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

background_path = os.path.join(BASE_DIR, "12.webp")
loading_path = os.path.join(BASE_DIR, "1356.jpeg")
background_form = pygame.image.load(os.path.join(BASE_DIR, "12.webp"))
loading_image = pygame.image.load(os.path.join(BASE_DIR, "1356.jpeg"))

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
background_form = pygame.transform.scale(background_form, (screen_width, screen_height))
loading_image = pygame.transform.scale(loading_image, (screen_width, screen_height))

# ------------------------------
# Gemini API Configuration Using Environment Variable
# ------------------------------

def configure_gemini_api(api_key):
    """
    Configure Gemini API client using the API key (new google-genai SDK)
    """
    return genai.Client(api_key=api_key)

def get_gemini_recommendation(test_summary):
    """
    Send a request to Gemini API and receive response using google-genai SDK
    """
    client = configure_gemini_api(GEMINI_API_KEY)
    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""
                Your vision test results summary:
                {test_summary}
                Please provide the analysis exactly in this format:
                Right Eye: <explanation>
                Left Eye: <explanation>
                Comparison of Right and Left: <concise summary>
                Amblyopia Risk (if yes, which eye?): <Yes/No and specify>
                Hyperopia or Myopia Risk: <Hyperopia/Myopia and explanation>
                Need to See a Doctor?: <Yes/No and details>
                Brief Conclusion: <short, actionable conclusion>
                You are a professional ophthalmologist and vision test specialist. 
                Please analyze the following patient data and provide a detailed, expert 
                assessment, including recommendations for further evaluation and care.
                """),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )
    try:
        response_text = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response_text += chunk.text
        return response_text
    except Exception as e:
        logging.error(f"Error in Gemini API call: {e}")
        # Return fallback recommendation to avoid error interruption
        return "No recommendation available due to internal API error."


# ------------------------------
# Multi-Camera Support and Specialized Hardware Functions
# ------------------------------
def get_available_cameras(max_test=5):
    available = []
    for index in range(max_test):
        cap = cv2.VideoCapture(index)
        if cap is not None and cap.read()[0]:
            available.append(index)
        cap.release()
    logging.info(f"Available cameras: {available}")
    return available

def select_camera():
    cameras = get_available_cameras()
    if not cameras:
        logging.error("No cameras available!")
        return None
    if len(cameras) == 1:
        logging.info(f"Using camera {cameras[0]}")
        return cameras[0]
    # If multiple cameras exist, ask user to select one
    print("Available cameras:")
    for cam in cameras:
        print(f"Camera number: {cam}")
    try:
        selected = int(input("Enter desired camera number: "))
        if selected in cameras:
            logging.info(f"Selected camera {selected}")
            return selected
        else:
            logging.info(f"Invalid camera number entered. Using default camera {cameras[0]}")
            return cameras[0]
    except Exception as e:
        logging.error(f"Error in camera selection: {e}")
        return cameras[0]

# ------------------------------
# Professional PDF Reporting Functions
# ------------------------------
def generate_comparison_text(user_folder, left_correct, left_incorrect, right_correct, right_incorrect):
    import os

    # Calculate count for each eye in current test
    curr_left_correct = len(left_correct)
    curr_left_incorrect = len(left_incorrect)
    curr_right_correct = len(right_correct)
    curr_right_incorrect = len(right_incorrect)

    # File storing previous results (for each eye)
    results_file = os.path.join(user_folder, "previous_results.txt")
    prev_left_correct, prev_left_incorrect, prev_right_correct, prev_right_incorrect = 0, 0, 0, 0
    if os.path.exists(results_file):
        try:
            with open(results_file, "r") as f:
                lines = f.readlines()
                if len(lines) >= 4:
                    prev_left_correct = int(lines[0].strip())
                    prev_left_incorrect = int(lines[1].strip())
                    prev_right_correct = int(lines[2].strip())
                    prev_right_incorrect = int(lines[3].strip())
        except Exception as e:
            logging.error(f"Error reading previous results: {e}")

    # Calculate changes
    diff_left_correct = curr_left_correct - prev_left_correct
    diff_left_incorrect = curr_left_incorrect - prev_left_incorrect
    diff_right_correct = curr_right_correct - prev_right_correct
    diff_right_incorrect = curr_right_incorrect - prev_right_incorrect

    # Generate comparison text
    text = f"--- Test Comparison Report ---\n\n"
    text += "Left Eye:\n"
    text += f"  Current - Correct: {curr_left_correct}, Incorrect: {curr_left_incorrect}\n"
    text += f"  Previous - Correct: {prev_left_correct}, Incorrect: {prev_left_incorrect}\n"
    text += f"  Change - Correct: {'+' if diff_left_correct>=0 else ''}{diff_left_correct}, Incorrect: {'+' if diff_left_incorrect>=0 else ''}{diff_left_incorrect}\n\n"
    
    text += "Right Eye:\n"
    text += f"  Current - Correct: {curr_right_correct}, Incorrect: {curr_right_incorrect}\n"
    text += f"  Previous - Correct: {prev_right_correct}, Incorrect: {prev_right_incorrect}\n"
    text += f"  Change - Correct: {'+' if diff_right_correct>=0 else ''}{diff_right_correct}, Incorrect: {'+' if diff_right_incorrect>=0 else ''}{diff_right_incorrect}\n\n"
    
    text += "Overall, the improvements/deteriorations are as listed above."

    # Save current results for future tests
    try:
        with open(results_file, "w") as f:
            f.write(f"{curr_left_correct}\n{curr_left_incorrect}\n{curr_right_correct}\n{curr_right_incorrect}")
    except Exception as e:
        logging.error(f"Error saving current results: {e}")

    return text


def upload_to_cloud(user_folder, pdf_filename):
    logging.info(f"Uploading {pdf_filename} from folder {user_folder} to the cloud...")
    # Here we can use a cloud API. For now, we just print a log message as an example
    # ...

# ------------------------------
# Helper Functions
# ------------------------------
def select_photo():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a photo",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    root.destroy()
    return file_path if file_path else None

# ------------------------------
# Graphics Settings (Settings Menu)
# ------------------------------
def is_first_run():
    # Check for a hidden config file in BASE_DIR
    config_flag = os.path.join(BASE_DIR, ".visiontest_configured")
    return not os.path.exists(config_flag)

def mark_configured(api_key, new_save_folder, fullscreen):
    settings_file = os.path.join(BASE_DIR, ".visiontest_settings.json")
    settings = {
         "api_key": api_key,
         "save_folder": new_save_folder,
         "fullscreen": fullscreen
    }
    try:
         with open(settings_file, "w") as f:
             json.dump(settings, f)
         logging.info("Settings saved successfully.")
    except Exception as e:
         logging.error(f"Error saving settings: {e}")

def compute_font_sizes(distance_m):
    """
    Calculate font size for each Snellen level based on distance.
    Stores both a baseline pixel size ('baseline_px') and the current
    'font_size_px' for each clinical_levels entry.
    """
    global mm_per_pixel
    if mm_per_pixel is None or mm_per_pixel <= 0:
        logging.error("mm_per_pixel not set or invalid")
        return clinical_levels

    # Visual angle for a 10/10 (baseline) optotype: 5 arc minutes (5/60 deg).
    # For a Snellen denominator 'd' (10/d), the optotype visual angle scales by d/10.
    min_baseline_px = 8  # sensible minimum baseline pixel size to keep legible

    for level_data in clinical_levels:
        # parse denominator from "10/XXX"
        try:
            denom = int(level_data["snellen"].split("/")[1])
        except Exception:
            denom = 10
        # visual angle in degrees for this Snellen level
        angle_deg = (5.0 / 60.0) * (denom / 10.0)
        # convert visual angle to physical height at distance (use small-angle formula):
        # height = 2 * distance * tan(angle/2)
        height_m = 2.0 * distance_m * math.tan(math.radians(angle_deg) / 2.0)
        height_mm = height_m * 1000.0
        px_size = max(min_baseline_px, int(round(height_mm / mm_per_pixel)))

        # store baseline and current values
        level_data["baseline_px"] = px_size
        level_data["font_size_px"] = px_size

        logging.info(f"Level {level_data['snellen']} baseline set to {px_size}px (height {height_mm:.2f} mm)")

    return clinical_levels



def load_settings():
    global GEMINI_API_KEY, save_folder, fullscreen_setting, screen_diag_in, mm_per_pixel
    # defaults
    if not GEMINI_API_KEY:
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    if 'save_folder' not in globals() or not globals()['save_folder']:
        save_folder = os.path.join(BASE_DIR, "results")
    if 'fullscreen_setting' not in globals():
        fullscreen_setting = True
    if 'screen_diag_in' not in globals() or not screen_diag_in:
        screen_diag_in = 15.0

    settings_file = os.path.join(BASE_DIR, ".visiontest_settings.json")
    try:
        if os.path.exists(settings_file):
            with open(settings_file, "r") as f:
                settings = json.load(f)
            GEMINI_API_KEY = settings.get("api_key", GEMINI_API_KEY)
            save_folder = settings.get("save_folder", save_folder)
            fullscreen_setting = settings.get("fullscreen", fullscreen_setting)
            screen_diag_in = float(settings.get("screen_diag_in", screen_diag_in))
    except Exception as e:
        logging.error(f"Error loading settings: {e}")

    info = pygame.display.Info()
    diag_pixels = math.sqrt(info.current_w**2 + info.current_h**2)

    if not isinstance(screen_diag_in, (int, float)) or screen_diag_in <= 0:
        screen_diag_in = 15.0

    dpi = diag_pixels / screen_diag_in
    mm_per_pixel = 25.4 / dpi
    logging.info(f"Settings loaded: screen_diag_in={screen_diag_in}, DPI={dpi:.2f}, mm_per_pixel={mm_per_pixel:.4f}")

def show_settings_menu():
    """
    Display settings menu with Tkinter including API Key input, Save Folder, Fullscreen and Screen Diagonal
    """
    import tkinter as tk
    from tkinter import filedialog

    def browse_folder():
        folder = filedialog.askdirectory(title="Select Folder for Saving Results")
        if folder:
            folder_var.set(folder)

    root = tk.Tk()
    root.title("Settings")

    api_key_var = tk.StringVar(value=GEMINI_API_KEY)
    folder_var = tk.StringVar(value=save_folder)
    fullscreen_var = tk.BooleanVar(value=fullscreen_setting)
    diag_var = tk.StringVar(value=str(screen_diag_in) if screen_diag_in is not None else "15")

    tk.Label(root, text="API Key:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Entry(root, textvariable=api_key_var, width=50).grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Save Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tk.Entry(root, textvariable=folder_var, width=50).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=5, pady=5)
    
    tk.Label(root, text="Fullscreen:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    tk.Checkbutton(root, variable=fullscreen_var).grid(row=2, column=1, sticky="w", padx=5, pady=5)
    
    tk.Label(root, text="Screen Diagonal (inches):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    tk.Entry(root, textvariable=diag_var, width=50).grid(row=3, column=1, padx=5, pady=5)

    def save_and_close():
        global GEMINI_API_KEY, save_folder, fullscreen_setting, screen_diag_in, mm_per_pixel
        GEMINI_API_KEY = api_key_var.get()
        save_folder = folder_var.get()
        fullscreen_setting = fullscreen_var.get()
        try:
            screen_diag_in = float(diag_var.get())
        except:
            screen_diag_in = 15.0
        
        # Calculate mm_per_pixel
        diag_pixels = math.sqrt(screen_width**2 + screen_height**2)
        dpi = diag_pixels / screen_diag_in
        mm_per_pixel = 25.4 / dpi
        logging.info(f"Settings saved: screen_diag_in={screen_diag_in}, DPI={dpi:.2f}, mm_per_pixel={mm_per_pixel:.4f}")
        
        # Save settings
        settings_file = os.path.join(BASE_DIR, ".visiontest_settings.json")
        settings = {
             "api_key": GEMINI_API_KEY,
             "save_folder": save_folder,
             "fullscreen": fullscreen_setting,
             "screen_diag_in": screen_diag_in
        }
        try:
             with open(settings_file, "w") as f:
                 json.dump(settings, f)
             logging.info("Settings saved successfully.")
             # Mark as configured so is_first_run() returns False next time
             config_flag = os.path.join(BASE_DIR, ".visiontest_configured")
             with open(config_flag, "w") as f:
                 f.write("configured")
        except Exception as e:
             logging.error(f"Error saving settings: {e}")
        root.destroy()
        # Reload settings after closing the dialog
        load_settings()
        # Optionally, you can force a redraw or update UI here if needed

    tk.Button(root, text="Save Settings", command=save_and_close).grid(row=4, column=0, columnspan=3, pady=10)
    root.mainloop()

# ------------------------------
# Camera Calibration with AR (Enhanced)
# ------------------------------
def calibrate_camera(camera_index=0, pattern_size=(9, 6), square_size=0.025, num_images=15):
    cap_calib = cv2.VideoCapture(camera_index)
    if not cap_calib.isOpened():
        logging.error("Unable to open camera!")
        return None, None

    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints, imgpoints = [], []
    count = 0
    logging.info("Starting camera calibration with AR overlay. Press SPACE to capture, 'q' to quit.")

    while count < num_images:
        ret, frame = cap_calib.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret_corners, corners = cv2.findChessboardCorners(gray, pattern_size, None)
        
        # Create an overlay to add AR elements
        overlay = frame.copy()
        if ret_corners:
            cv2.drawChessboardCorners(overlay, pattern_size, corners, ret_corners)
            cv2.putText(overlay, f"Captured: {count}/{num_images}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(overlay, (int(x), int(y)), 5, (255, 0, 0), -1)
        else:
            cv2.putText(overlay, "Chessboard not detected. Adjust position.", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow("Calibration AR", overlay)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            if ret_corners:
                objpoints.append(objp)
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1),
                    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                )
                imgpoints.append(corners2)
                count += 1
                logging.info(f"Captured image {count}.")
            else:
                logging.info("Chessboard not detected. Image not captured.")
        elif key == ord('q'):
            break

    cap_calib.release()
    cv2.destroyAllWindows()

    if len(objpoints) < 3:
        logging.error("Not enough images captured for calibration!")
        return None, None

    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )
    if ret:
        focal_length = camera_matrix[0, 0]  # From calibration matrix
        camera_name = f"camera_{camera_index}"
        focals_file = os.path.join(BASE_DIR, "camera_focals.json")
        try:
            if os.path.exists(focals_file):
                with open(focals_file, "r") as f:
                    focals_data = json.load(f)
            else:
                focals_data = {}
            focals_data[camera_name] = focal_length
            with open(focals_file, "w") as f:
                json.dump(focals_data, f)
            logging.info(f"Focal length {focal_length} saved for {camera_name}.")
        except Exception as e:
            logging.error(f"Error saving focal length: {e}")
        logging.info("Camera calibration successful.")
        return camera_matrix, dist_coeffs
    else:
        logging.error("Camera calibration failed.")
        return None, None

# ------------------------------
# Initial Pygame UI Setup
# ------------------------------
# Set default fullscreen setting before loading persisted settings
fullscreen_setting = True
screen_diag_in = 15.0
load_settings()  # load settings before creating the screen
flags = pygame.FULLSCREEN if fullscreen_setting else 0
screen = pygame.display.set_mode((screen_width, screen_height), flags)
pygame.display.set_caption("M-Tech Clinical Vision Test")
BASE_WIDTH, BASE_HEIGHT = 800, 600
scale_factor = screen_height / BASE_HEIGHT

def get_scaled_font(size):
    # Using the average of the horizontal and vertical scale factors based on a base resolution.
    avg_scale = ((screen_width / BASE_WIDTH) + (screen_height / BASE_HEIGHT)) / 2
    return pygame.font.SysFont(None, int(size * avg_scale))

WHITE, BLACK = (255, 255, 255), (0, 0, 0)

clinical_levels = [
    {"snellen": "10/200"},
    {"snellen": "10/160"},
    {"snellen": "10/125"},
    {"snellen": "10/100"},
    {"snellen": "10/80"},
    {"snellen": "10/70"},
    {"snellen": "10/60"},
    {"snellen": "10/50"},
    {"snellen": "10/40"},
    {"snellen": "10/30"},
    {"snellen": "10/25"},
    {"snellen": "10/20"},
    {"snellen": "10/15"},
    {"snellen": "10/10"},
]
test_distance = 1  # Standard test distance in meters


mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
cap = None  # Will be initialized after camera selection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

calibrated_camera_matrix = None
calibrated_dist_coeffs = None

user_name = user_surname = user_age = ""
national_id = ""
phone = ""
email = ""
photo_path = None
left_eye_correct, left_eye_incorrect = [], []
right_eye_correct, right_eye_incorrect = [], []
gemini_recommendation = "No recommendation."

def crop_to_square(frame):
    h, w, _ = frame.shape
    side = min(w, h)
    start_x = (w - side) // 2
    start_y = (h - side) // 2
    return frame[start_y:start_y+side, start_x:start_x+side]

def get_finger_direction(landmarks, mcp_index, tip_index):
    mcp = landmarks.landmark[mcp_index]
    tip = landmarks.landmark[tip_index]
    dx, dy = tip.x - mcp.x, tip.y - mcp.y
    angle = math.degrees(math.atan2(-dy, dx))
    angle = angle if angle >= 0 else angle + 360
    if angle >= 315 or angle < 45:
        return 0
    elif 45 <= angle < 135:
        return 90
    elif 135 <= angle < 225:
        return 180
    else:
        return 270

def get_extended_hand_direction(frame):
    square_frame = crop_to_square(frame)
    frame_rgb = cv2.cvtColor(square_frame, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(frame_rgb)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        h, w, _ = square_frame.shape
        xs = [lm.x for lm in hand_landmarks.landmark]
        ys = [lm.y for lm in hand_landmarks.landmark]
        hand_center_x = sum(xs) / len(xs) * w
        hand_center_y = sum(ys) / len(ys) * h

        face_results = face_detection.process(frame_rgb)
        if face_results.detections:
            detection = face_results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            face_x = bbox.xmin * w
            face_y = bbox.ymin * h
            face_width = bbox.width * w
            face_height = bbox.height * h
            if face_x <= hand_center_x <= face_x + face_width and face_y <= hand_center_y <= face_y + face_height:
                return None

        directions = []
        for mcp, tip in [(5, 8), (9, 12), (13, 16), (17, 20)]:
            directions.append(get_finger_direction(hand_landmarks, mcp, tip))
        return Counter(directions).most_common(1)[0][0]
    return None

def average_hand_direction(duration=0.5):
    samples = []
    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        direction = get_extended_hand_direction(frame)
        if direction is not None:
            samples.append(direction)
        time.sleep(0.05)
    return Counter(samples).most_common(1)[0][0] if samples else None

def render_letter(letter_surface):
    rect = letter_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    if rect.width > screen_width or rect.height > screen_height:
        scale = min(screen_width / rect.width, screen_height / rect.height)
        new_size = (int(rect.width * scale), int(rect.height * scale))
        letter_surface = pygame.transform.scale(letter_surface, new_size)
        rect = letter_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    return letter_surface, rect

def detect_distance():
    ret, frame = cap.read()
    if not ret:
        logging.error("Unable to read frame from camera.")
        return test_distance
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detection.process(frame_rgb)
    if results.detections:
        detection = results.detections[0]
        bbox = detection.location_data.relative_bounding_box
        h, w, _ = frame.shape
        face_width = bbox.width * w
        REAL_FACE_WIDTH = 0.16  # Real face width in meters
        focals_file = os.path.join(BASE_DIR, "camera_focals.json")
        if os.path.exists(focals_file):
            try:
                with open(focals_file, "r") as f:
                    focals_data = json.load(f)
                focal_length = next(iter(focals_data.values()), 700)
                logging.info(f"Loaded saved focal length: {focal_length}")
            except Exception as e:
                logging.error(f"Error reading focals file: {e}")
                focal_length = 700
        else:
            focal_length = 700
        if face_width <= 1e-6:
            logging.error("Detected face width too small; using default distance.")
            return test_distance
        distance = (REAL_FACE_WIDTH * focal_length) / face_width
        logging.info(f"Measured distance: {distance:.2f} meters")
        return distance
    logging.info("No face detected, using default distance.")
    return test_distance

def adjust_font_sizes(measured_distance):
    """
    Scale font_size_px for each level from the stored 'baseline_px' according to measured_distance.
    This preserves relative differences between levels.
    """
    if measured_distance <= 0:
        logging.error("Measured distance invalid; skipping font size adjustment.")
        return

    scale = measured_distance / test_distance
    logging.info(f"Scale factor: {scale:.2f}")

    for level in clinical_levels:
        baseline = level.get("baseline_px", level.get("font_size_px", 8))
        # Ensure baseline is at least 1
        baseline = max(1, int(baseline))
        new_px = max(int(round(baseline * scale)), 5)  # enforce a minimum visible size
        level["font_size_px"] = new_px
        logging.info(f"Level {level['snellen']} adjusted from baseline {baseline}px to {new_px}px")


def display_logo():
    # Modern, minimal, and fresh game-like splash with gradients and glassmorphism
    # Draw a diagonal blue-to-cyan gradient background (fast version)
    bg_surface = pygame.Surface((screen_width, screen_height))
    arr = pygame.surfarray.pixels3d(bg_surface)
    for y in range(screen_height):
        for x in range(screen_width):
            t = (x + y) / (screen_width + screen_height)
            r = int(10 * (1 - t) + 0 * t)
            g = int(120 * (1 - t) + 220 * t)
            b = int(220 * (1 - t) + 255 * t)
            arr[x, y] = (r, g, b)
    del arr
    screen.blit(bg_surface, (0, 0))

    # Glassmorphism effect: semi-transparent frosted glass panel
    glass_width, glass_height = 500, 260
    glass_surface = pygame.Surface((glass_width, glass_height), pygame.SRCALPHA)
    glass_surface.fill((255, 255, 255, 60))
    pygame.draw.rect(glass_surface, (255, 255, 255, 90), (0, 0, glass_width, glass_height), border_radius=32)
    glass_rect = glass_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 10))
    screen.blit(glass_surface, glass_rect)

    # Neon border for glass panel
    pygame.draw.rect(screen, (0, 255, 255), glass_rect, 4, border_radius=32)

    # Modern abstract eye (flat style)
    eye_center = (screen_width // 2, screen_height // 2 - 40)
    pygame.draw.ellipse(screen, (255, 255, 255, 220), (eye_center[0] - 90, eye_center[1] - 36, 180, 72))
    pygame.draw.ellipse(screen, (0, 180, 255), (eye_center[0] - 60, eye_center[1] - 24, 120, 48))
    pygame.draw.circle(screen, (30, 30, 30), eye_center, 18)
    pygame.draw.circle(screen, (255, 255, 255), (eye_center[0] - 7, eye_center[1] - 7), 5)

    # Neon accent line under the eye
    pygame.draw.arc(screen, (0, 255, 255), (eye_center[0] - 70, eye_center[1] + 20, 140, 40), 3.5, 6.0, 4)

    # Title and subtitle with modern font and neon shadow
    main_font = get_scaled_font(78)
    sub_font = get_scaled_font(28)
    main_text = main_font.render("Vision Test", True, (0, 40, 80))
    neon_shadow = main_font.render("Vision Test", True, (0, 255, 255))
    screen.blit(neon_shadow, neon_shadow.get_rect(center=(screen_width//2 + 3, screen_height//2 + 65)))
    screen.blit(main_text, main_text.get_rect(center=(screen_width//2, screen_height//2 + 60)))
    sub_text = sub_font.render("Created by M-Tech", True, (0, 120, 180))
    screen.blit(sub_text, sub_text.get_rect(center=(screen_width//2, screen_height//2 + 110)))

    pygame.display.flip()
    pygame.time.wait(2000)

def show_instructions():
    # Use a blue panel for instructions
    panel_surface = pygame.Surface((600, 220), pygame.SRCALPHA)
    panel_surface.fill((255, 255, 255, 235))
    panel_rect = panel_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.fill(WHITE)
    font = get_scaled_font(30)
    instructions = [
        "• Cover one eye as instructed.",
        "• Point your hand in the given direction.",
        "• Results will be saved after testing both eyes."
    ]
    screen.blit(panel_surface, panel_rect)
    for i, line in enumerate(instructions):
        screen.blit(font.render(line, True, (0, 51, 102)), (panel_rect.left + 30, panel_rect.top + 30 + i * 45))
    pygame.display.flip()
    pygame.time.wait(3000)

def compare_with_previous_results(user_folder):
    logging.info(f"Comparing current results with previous tests in folder: {user_folder}")
    previous_files = [f for f in os.listdir(user_folder) if f.endswith('.pdf')]
    if previous_files:
        logging.info(f"Found {len(previous_files)} previous test file(s).")
    else:
        logging.info("No previous tests found.")

def show_form(manager):
    # Draw a semi-transparent white panel for the form
    panel_surface = pygame.Surface((600, 480), pygame.SRCALPHA)
    panel_surface.fill((255, 255, 255, 220))  # semi-transparent white
    panel_rect = panel_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    screen.blit(background_form, (0, 0))
    screen.blit(panel_surface, panel_rect)

    # Draw a blue medical header with a stethoscope icon (if available)
    header_rect = pygame.Rect(panel_rect.left, panel_rect.top, panel_rect.width, 60)
    pygame.draw.rect(screen, (0, 102, 204), header_rect, border_radius=15)
    header_font = get_scaled_font(36)
    header_text = header_font.render("Patient Registration", True, (255, 255, 255))
    screen.blit(header_text, (header_rect.left + 20, header_rect.top + 12))
    # Optional: draw a cross icon or stethoscope if you have an icon file
    # icon = pygame.image.load(os.path.join(BASE_DIR, "stethoscope.png"))
    # icon = pygame.transform.scale(icon, (36, 36))
    # screen.blit(icon, (header_rect.right - 56, header_rect.top + 12))

    # Draw a thin blue border around the panel
    pygame.draw.rect(screen, (0, 102, 204), panel_rect, 3, border_radius=18)

    # Place form fields on the panel
    base_x = panel_rect.left + 40
    base_y = panel_rect.top + 80
    spacing = 48

    name_entry = UITextEntryLine(pygame.Rect((base_x, base_y), (panel_rect.width - 80, 36)), manager, placeholder_text='Enter your Name')
    surname_entry = UITextEntryLine(pygame.Rect((base_x, base_y + spacing), (panel_rect.width - 80, 36)), manager, placeholder_text='Enter your Surname')
    age_entry = UITextEntryLine(pygame.Rect((base_x, base_y + 2 * spacing), (panel_rect.width - 80, 36)), manager, placeholder_text='Enter your Age')
    national_id_entry = UITextEntryLine(pygame.Rect((base_x, base_y + 3 * spacing), (panel_rect.width - 80, 36)), manager, placeholder_text='Enter your National ID (Optional)')
    phone_entry = UITextEntryLine(pygame.Rect((base_x, base_y + 4 * spacing), (panel_rect.width - 80, 36)), manager, placeholder_text='Enter your Phone Number (Optional)')
    email_entry = UITextEntryLine(pygame.Rect((base_x, base_y + 5 * spacing), (panel_rect.width - 80, 36)), manager, placeholder_text='Enter your Email (Optional)')
    photo_button = UIButton(pygame.Rect((base_x, base_y + 6 * spacing), (panel_rect.width - 80, 36)), 'Upload Photo (Optional)', manager)
    submit_button = UIButton(pygame.Rect((base_x, base_y + 7 * spacing), (panel_rect.width - 80, 36)), 'Submit', manager)
    start_test_button = UIButton(pygame.Rect((base_x, base_y + 8 * spacing), (panel_rect.width - 80, 36)), 'Start Integrated Vision Test', manager)
    start_test_button.visible = False

    pygame.display.flip()

    return {
        "name_entry": name_entry,
        "surname_entry": surname_entry,
        "age_entry": age_entry,
        "national_id_entry": national_id_entry,
        "phone_entry": phone_entry,
        "email_entry": email_entry,
        "photo_button": photo_button,
        "submit_button": submit_button,
        "start_test_button": start_test_button
    }

def save_results(user_name, user_surname, user_age, national_id, phone, email,
                 left_correct, left_incorrect, right_correct, right_eye_incorrect,
                 recommendation, photo_path=None):
    # Updated to use save_folder for saving results
    folder_name = os.path.join(save_folder, f"{user_name}_{user_surname}")
    os.makedirs(folder_name, exist_ok=True)

    # Use the correct parameter name for right eye incorrect levels
    comparison_text = generate_comparison_text(folder_name, left_correct, left_incorrect, right_correct, right_eye_incorrect)  # type: ignore
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = os.path.join(folder_name, f"vision_test_{timestamp}.pdf")
    try:
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        styles = getSampleStyleSheet()

        # recommendation
        rec_lower = recommendation.lower()
        if "risk" in rec_lower or "abnormal" in rec_lower:
            color = "red"
        elif "no significant" in rec_lower:
            color = "green"
        else:
            color = "black"

        # Format recommendation with HTML breaks for better readability.
        formatted_recommendation = '<br/>'.join(recommendation.strip().splitlines())
        recommendation_formatted = f'<font color="{color}">{formatted_recommendation}</font>'

        elements = [
            Paragraph(f"Name: {user_name}", styles['Normal']),
            Paragraph(f"Surname: {user_surname}", styles['Normal']),
            Paragraph(f"Age: {user_age}", styles['Normal']),
            Paragraph(f"National ID: {national_id if national_id else 'N/A'}", styles['Normal']),
            Paragraph(f"Phone: {phone if phone else 'N/A'}", styles['Normal']),
            Paragraph(f"Email: {email if email else 'N/A'}", styles['Normal']),
            Paragraph("Left Eye:", styles['Normal']),
            Paragraph(f"  Correct Levels: {', '.join(left_correct) if left_correct else 'None'}", styles['Normal']),
            Paragraph(f"  Incorrect Levels: {', '.join(left_incorrect) if left_incorrect else 'None'}", styles['Normal']),
            Paragraph("Right Eye:", styles['Normal']),
            Paragraph(f"  Correct Levels: {', '.join(right_correct) if right_correct else 'None'}", styles['Normal']),
            Paragraph(f"  Incorrect Levels: {', '.join(right_eye_incorrect) if right_eye_incorrect else 'None'}", styles['Normal']),
            Paragraph("Recommendation:", styles['Normal']),
            Paragraph(recommendation_formatted, styles['Normal']),
            Paragraph("Comparison with previous tests:", styles['Normal']),
        ]

        # Add comparison text (it's a textual summary, not a file path)
        elements.append(Paragraph(comparison_text.replace("\n", "<br/>"), styles['Normal']))
        # If a photo exists, attach it
        if photo_path and os.path.exists(photo_path):
            try:
                elements.append(Image(photo_path, width=2*inch, height=2*inch))
            except Exception as e:
                logging.error(f"Error adding photo to PDF: {e}")
        doc.build(elements)
        logging.info("Results saved successfully as PDF.")
    except Exception as e:
        logging.error(f"Error saving results as PDF: {e}")

    upload_to_cloud(folder_name, pdf_filename)

def wait_for_stable_hand(manager, stable_time=1.5, current_image=None):
    stable_direction, start_stable = None, None
    start_time = time.time()
    warning_font = get_scaled_font(30)

    # Mapping English directions
    direction_mapping = {
        0: "Right",
        90: "Up",
        180: "Left",
        270: "Down"
    }

    while True:
        direction = average_hand_direction(duration=0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                cap.release()
                exit()
            elif event.type == pygame.KEYDOWN:
                # Return immediately on key press
                if event.key == pygame.K_UP:
                    return 90
                elif event.key == pygame.K_RIGHT:
                    return 0
                elif event.key == pygame.K_DOWN:
                    return 270
                elif event.key == pygame.K_LEFT:
                    return 180
            manager.process_events(event)
        if direction is None and time.time() - start_time > 10:
            pygame.draw.rect(screen, WHITE, (0, screen_height - 100, screen_width, 100))
            screen.blit(warning_font.render("No hand, voice, or keyboard input detected!", True, (255, 0, 0)), (100, screen_height - 80))
        elif direction is not None:
            pygame.draw.rect(screen, WHITE, (0, screen_height - 100, screen_width, 100))
            direction_text = direction_mapping.get(direction, str(direction))
            screen.blit(warning_font.render(f"Hand detected: {direction_text}", True, (0, 255, 0)), (100, screen_height - 80))
            if stable_direction != direction:
                stable_direction, start_stable = direction, time.time()
            elif time.time() - start_stable >= stable_time:
                return direction
        if current_image:
            img_rect = current_image.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(current_image, img_rect)
        manager.update(0.01)
        manager.draw_ui(screen)
        pygame.display.update()

def perform_full_test_for_eye(eye, manager, measured_distance):
    prompt_font = get_scaled_font(30)
    screen.fill(WHITE)
    prompt_text = f"Please cover your {eye} eye for the test"
    screen.blit(prompt_font.render(prompt_text, True, BLACK), (200, 250))
    pygame.display.flip()
    pygame.time.wait(3000)

    correct_levels, incorrect_levels = [], []
    for level_data in clinical_levels:
        font_size = level_data["font_size_px"]          
        snellen_ratio = level_data["snellen"]
        expected_direction = random.choice([0, 90, 180, 270])
        # Change to use Optotype font
        font = get_optotype_font(font_size)
        letter_surface = font.render("E", True, BLACK)
        letter_surface, rect = render_letter(letter_surface)
        rotated_surface = pygame.transform.rotate(letter_surface, expected_direction)

        screen.fill(WHITE)
        screen.blit(prompt_font.render(f"Level: {snellen_ratio}", True, BLACK), (10, 10))
        screen.blit(prompt_font.render(f"Adjusted to distance: {measured_distance:.2f} m", True, BLACK), (10, 40))
        rect = rotated_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(rotated_surface, rect)
        manager.update(0.01)
        manager.draw_ui(screen)
        pygame.display.flip()

        stable_dir = wait_for_stable_hand(manager, stable_time=1.5, current_image=rotated_surface)
        if stable_dir == expected_direction:
            correct_levels.append(snellen_ratio)
        else:
            incorrect_levels.append(snellen_ratio)
        pygame.time.wait(500)
    return correct_levels, incorrect_levels

def main():
    global user_name, user_surname, user_age, national_id, phone, email, photo_path
    global left_eye_correct, left_eye_incorrect, right_eye_correct, right_eye_incorrect, gemini_recommendation
    global calibrated_camera_matrix, calibrated_dist_coeffs, cap, clinical_levels  # added clinical_levels

    # Select camera from available cameras
    selected_camera = select_camera()
    if selected_camera is None:
        logging.error("No available camera found. Exiting.")
        return
    cap = cv2.VideoCapture(selected_camera)

    # Load settings and calculate screen-related values
    load_settings()
    info = pygame.display.Info()
    diag_pixels = math.sqrt(screen_width**2 + screen_height**2)
    dpi = diag_pixels / screen_diag_in
    mm_per_pixel = 25.4 / dpi
    logging.info(f"In main: screen_diag_in={screen_diag_in}, DPI={dpi:.2f}, mm_per_pixel={mm_per_pixel:.4f}")
    clinical_levels = compute_font_sizes(test_distance)


    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((screen_width, screen_height))

    # Load your custom icon for settings (PNG recommended, relative to BASE_DIR)
    # Change the filename below to your desired icon image (e.g. "my_icon.png")
    settings_icon_path = os.path.join(BASE_DIR, "assets", "settings_icon.png")  # use local assets/settings_icon.png if available
    if os.path.exists(settings_icon_path):
        settings_icon_surface = pygame.image.load(settings_icon_path).convert_alpha()
        settings_icon_surface = pygame.transform.smoothscale(settings_icon_surface, (52, 52))
    else:
        settings_icon_surface = None

    # Create a UIButton with no text and custom icon as background
    settings_button = UIButton(
        pygame.Rect(10, 10, 48, 48),
        '',
        manager,
        object_id="#settings_icon_button"
    )

    display_logo()
    # Show settings menu on first run
    if is_first_run():
        show_settings_menu()
    ui_elements = show_form(manager)
    user_details_collected = False
    in_test = False
    measured_distance = test_distance

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                if cap.isOpened():
                    cap.release()
                return
            
            # Process settings button event
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == settings_button:
                    show_settings_menu()
            manager.process_events(event)
            if not user_details_collected:
                if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ui_elements["photo_button"]:
                        photo_path = select_photo()
                    elif event.ui_element == ui_elements["submit_button"]:
                        user_name = ui_elements["name_entry"].get_text().strip()
                        user_surname = ui_elements["surname_entry"].get_text().strip()
                        user_age = ui_elements["age_entry"].get_text().strip()
                        national_id = ui_elements["national_id_entry"].get_text().strip()
                        phone = ui_elements["phone_entry"].get_text().strip()
                        email = ui_elements["email_entry"].get_text().strip()
                        if user_name and user_surname and user_age.isdigit():
                            user_details_collected = True
                            ui_elements["start_test_button"].visible = True
                            logging.info(f"Patient registered: {user_name} {user_surname}, Age: {user_age}")
                        else:
                            logging.warning("Please enter name, surname and age correctly")
                            print("Please enter name, surname and age correctly")
            elif user_details_collected and not in_test:
                if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == ui_elements["start_test_button"]:
                        in_test = True
                        for element in list(ui_elements.values()):
                            element.kill()
                        show_instructions()
                        logging.info("Starting camera calibration...")
                        calibrated_camera_matrix, calibrated_dist_coeffs = calibrate_camera(selected_camera)
                        if calibrated_camera_matrix is not None:
                            focal_length = calibrated_camera_matrix[0, 0]
                            logging.info(f"✓ Calibration successful - Focal length: {focal_length:.2f}px")
                        else:
                            logging.warning("✗ Calibration failed. Using default values.")
                        measured_distance = detect_distance()
                        screen.fill(WHITE)
                        distance_text = get_scaled_font(30).render(f"Measured Distance: {measured_distance:.2f} m", True, BLACK)
                        screen.blit(distance_text, (200, 200))
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        adjust_font_sizes(measured_distance)
            else:
                # Safely remove all UI elements. LayeredGUIGroup is not iterable,
                # so get children from the manager's root container. Provide a
                # sprite-list fallback for older/newer pygame_gui versions.
                try:
                    children = manager.get_root_container().get_children()
                    for element in list(children):
                        try:
                            element.kill()
                        except Exception:
                            pass
                except Exception:
                    # Fallback: try iterating sprite list if available
                    try:
                        for sprite in getattr(manager.ui_group, "sprites", lambda: [])():
                            try:
                                sprite.kill()
                            except Exception:
                                pass
                    except Exception:
                        # As a last resort, ignore and continue
                        pass
                left_eye_correct, left_eye_incorrect = perform_full_test_for_eye("left", manager, measured_distance)
                right_eye_correct, right_eye_incorrect = perform_full_test_for_eye("right", manager, measured_distance)

                # Log test results
                logging.info(f"Left Eye - Correct: {', '.join(left_eye_correct) if left_eye_correct else 'None'}")
                logging.info(f"Left Eye - Incorrect: {', '.join(left_eye_incorrect) if left_eye_incorrect else 'None'}")
                logging.info(f"Right Eye - Correct: {', '.join(right_eye_correct) if right_eye_correct else 'None'}")
                logging.info(f"Right Eye - Incorrect: {', '.join(right_eye_incorrect) if right_eye_incorrect else 'None'}")

                test_summary = (
                    f"Left Eye - Correct Levels: {', '.join(left_eye_correct) if left_eye_correct else 'None'}\n"
                    f"Left Eye - Incorrect Levels: {', '.join(left_eye_incorrect) if left_eye_incorrect else 'None'}\n"
                    f"Right Eye - Correct Levels: {', '.join(right_eye_correct) if right_eye_correct else 'None'}\n"
                    f"Right Eye - Incorrect Levels: {', '.join(right_eye_incorrect) if right_eye_incorrect else 'None'}"
                )
                ml_analysis = "No significant abnormalities detected."
                if "10/200" in test_summary or "10/160" in test_summary:
                    ml_analysis = "Possible risk of glaucoma. Recommend further ophthalmologic evaluation."
                logging.info(f"ML Analysis: {ml_analysis}")
                test_summary += f"\nML Analysis: {ml_analysis}"

                screen.blit(loading_image, (0, 0))
                loading_text = get_scaled_font(40).render("Generating AI recommendation...", True, BLACK)
                screen.blit(loading_text, (screen_width//2 - loading_text.get_width()//2, screen_height//2 - loading_text.get_height()//2))
                pygame.display.flip()
                pygame.time.wait(3000)

                gemini_recommendation = get_gemini_recommendation(test_summary)
                # If the API returns a fallback message, replace it with local ML analysis
                if "No recommendation available" in gemini_recommendation:
                    gemini_recommendation = ml_analysis
                logging.info("Saving test results...")
                user_folder = f"{user_name}_{user_surname}"
                if os.path.exists(user_folder):
                    compare_with_previous_results(user_folder)
                save_results(user_name, user_surname, user_age, national_id, phone, email,
                             left_eye_correct, left_eye_incorrect, right_eye_correct, right_eye_incorrect,
                             gemini_recommendation, photo_path)
                logging.info("Test completed and results saved successfully")

                screen.fill(WHITE)
                complete_text = get_scaled_font(30).render("Test completed. Results saved.", True, BLACK)
                screen.blit(complete_text, (200, 200))
                pygame.display.flip()
                pygame.time.wait(3000)
                if cap.isOpened():
                    cap.release()
                cap = cv2.VideoCapture(selected_camera)
                left_eye_correct, left_eye_incorrect = [], []
                right_eye_correct, right_eye_incorrect = [], []
                in_test, user_details_collected = False, False
                ui_elements = show_form(manager)
        # Always draw the background before drawing UI elements
        screen.blit(background_form, (0, 0))
        manager.update(time_delta)
        manager.draw_ui(screen)

        # Draw the icon exactly centered on the button rect (not top-left of button)
        if settings_icon_surface:
            # Draw icon centered over the button, allow for larger icon (may overlap a bit for effect)
            icon_rect = settings_icon_surface.get_rect(center=(10 + 24, 10 + 24))
            screen.blit(settings_icon_surface, icon_rect)

        pygame.display.update()

if __name__ == "__main__":
    main()