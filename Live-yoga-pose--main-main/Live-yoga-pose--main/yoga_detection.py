import cv2
import sys
import numpy as np
import time
from tkinter import messagebox
from database import add_session
from pose_classifier import load_yoga_model, classify_pose
from feedback import FeedbackEngine, generate_feedback

# Lazy-load mediapipe modules
mp_pose = None
mp_drawing = None

def open_camera():
    for idx in range(0, 4):
        cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
        cap.release()
    return None

def _init_mediapipe():
    global mp_pose, mp_drawing
    if mp_pose is not None:
        return
    try:
        import mediapipe as mp
        mp_pose = mp.solutions.pose
        mp_drawing = mp.solutions.drawing_utils
    except (ImportError, AttributeError) as e:
        print(f"Error initializing mediapipe: {e}")
        print("Attempting alternative import method...")
        raise


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
    return angle


def extract_pose_angles(landmarks, image_width, image_height):
    _init_mediapipe()  # Initialize mediapipe when needed
    def get_point(key):
        lm = landmarks[key]
        return [lm.x * image_width, lm.y * image_height]

    points = {}
    indices = {
        "left_shoulder": mp_pose.PoseLandmark.LEFT_SHOULDER,
        "right_shoulder": mp_pose.PoseLandmark.RIGHT_SHOULDER,
        "left_elbow": mp_pose.PoseLandmark.LEFT_ELBOW,
        "right_elbow": mp_pose.PoseLandmark.RIGHT_ELBOW,
        "left_wrist": mp_pose.PoseLandmark.LEFT_WRIST,
        "right_wrist": mp_pose.PoseLandmark.RIGHT_WRIST,
        "left_hip": mp_pose.PoseLandmark.LEFT_HIP,
        "right_hip": mp_pose.PoseLandmark.RIGHT_HIP,
        "left_knee": mp_pose.PoseLandmark.LEFT_KNEE,
        "right_knee": mp_pose.PoseLandmark.RIGHT_KNEE,
        "left_ankle": mp_pose.PoseLandmark.LEFT_ANKLE,
        "right_ankle": mp_pose.PoseLandmark.RIGHT_ANKLE,
    }

    for name, landmark_id in indices.items():
        points[name] = get_point(landmark_id)

    angles = {
        "left_elbow_angle": calculate_angle(points["left_shoulder"], points["left_elbow"], points["left_wrist"]),
        "right_elbow_angle": calculate_angle(points["right_shoulder"], points["right_elbow"], points["right_wrist"]),
        "left_shoulder_angle": calculate_angle(points["left_elbow"], points["left_shoulder"], points["left_hip"]),
        "right_shoulder_angle": calculate_angle(points["right_elbow"], points["right_shoulder"], points["right_hip"]),
        "left_hip_angle": calculate_angle(points["left_shoulder"], points["left_hip"], points["left_knee"]),
        "right_hip_angle": calculate_angle(points["right_shoulder"], points["right_hip"], points["right_knee"]),
        "left_knee_angle": calculate_angle(points["left_hip"], points["left_knee"], points["left_ankle"]),
        "right_knee_angle": calculate_angle(points["right_hip"], points["right_knee"], points["right_ankle"]),
        "back_angle": calculate_angle(points["left_shoulder"], points["left_hip"], points["left_ankle"]),
    }
    return angles


def display_overlay(frame, pose_name, score, feedback_text):
    cv2.rectangle(frame, (0, 0), (frame.shape[1], 110), (10, 10, 10), -1)
    cv2.putText(frame, f"Pose: {pose_name}", (12, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (170, 255, 195), 2)
    cv2.putText(frame, f"Accuracy: {score:.1f}%", (12, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (170, 255, 195), 2)
    cv2.putText(frame, f"Feedback: {feedback_text}", (12, 92), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (235, 235, 235), 2)


def start_yoga_evaluation(username):
    try:
        _init_mediapipe()  # Initialize mediapipe when function is called
    except Exception as e:
        messagebox.showerror("Mediapipe Error", f"Yoga evaluation cannot start because MediaPipe failed to initialize:\n{e}")
        return

    model = load_yoga_model()
    feedback_engine = FeedbackEngine()
    capture = open_camera()

    if capture is None:
        messagebox.showerror("Camera Error", "Cannot open webcam. Please check that your camera is connected, not in use by another app, and try again.")
        return

    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        session_start = time.time()
        accumulated_score = 0.0
        frame_count = 0
        last_feedback = ""
        last_pose = "Unknown"

        while True:
            success, frame = capture.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            image_height, image_width = frame.shape[:2]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            pose_name = "Searching..."
            accuracy = 0.0
            feedback_text = "Move into one of the supported yoga poses"

            if results.pose_landmarks:
                angles = extract_pose_angles(results.pose_landmarks.landmark, image_width, image_height)
                pose_name, accuracy = classify_pose(model, angles)
                feedback_list = generate_feedback(pose_name, angles)
                feedback_text = feedback_list[0] if feedback_list else "Good posture"

                if feedback_text != last_feedback:
                    feedback_engine.speak(feedback_text)
                    last_feedback = feedback_text

                last_pose = pose_name
                accumulated_score += accuracy
                frame_count += 1
                display_overlay(frame, pose_name, accuracy, feedback_text)
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            else:
                display_overlay(frame, pose_name, accuracy, feedback_text)

            cv2.imshow("AI Yoga Posture Evaluation", frame)
            key = cv2.waitKey(1)
            if key == ord("q") or key == 27:
                break

        capture.release()
        cv2.destroyAllWindows()

        if frame_count > 0:
            average_accuracy = accumulated_score / frame_count
        else:
            average_accuracy = 0.0

        session_duration = int(time.time() - session_start)
        add_session(username, last_pose, round(average_accuracy, 2), session_duration, last_feedback)
        feedback_engine.speak(f"Session saved with average accuracy {average_accuracy:.1f} percent")
