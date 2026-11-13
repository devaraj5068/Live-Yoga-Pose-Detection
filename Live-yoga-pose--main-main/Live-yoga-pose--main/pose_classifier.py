import os
import pickle
import numpy as np

try:
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

MODEL_H5 = os.path.join("model", "yoga_model.h5")
MODEL_PKL = os.path.join("model", "yoga_model.pkl")
POSE_CLASSES = [
    "Mountain Pose",
    "Tree Pose",
    "Warrior Pose",
    "Triangle Pose",
    "Cobra Pose",
]


def load_yoga_model():
    if TENSORFLOW_AVAILABLE and os.path.exists(MODEL_H5):
        try:
            return keras.models.load_model(MODEL_H5)
        except Exception as e:
            print(f"Could not load TensorFlow model: {e}")
    if os.path.exists(MODEL_PKL):
        try:
            with open(MODEL_PKL, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Could not load sklearn model: {e}")
    return None


def get_pose_name(label):
    if label is None or label < 0 or label >= len(POSE_CLASSES):
        return "Unknown"
    return POSE_CLASSES[int(label)]


def normalize_features(features):
    arr = np.array(features, dtype=np.float32)
    if np.max(arr) > 0:
        return arr / (np.max(arr) + 1e-6)
    return arr


def classify_pose(model, angles):
    if model is None:
        return "Unknown", 0.0
    feature_vector = np.array([
        angles.get("left_elbow_angle", 0),
        angles.get("right_elbow_angle", 0),
        angles.get("left_shoulder_angle", 0),
        angles.get("right_shoulder_angle", 0),
        angles.get("left_hip_angle", 0),
        angles.get("right_hip_angle", 0),
        angles.get("left_knee_angle", 0),
        angles.get("right_knee_angle", 0),
        angles.get("back_angle", 0),
    ], dtype=np.float32)
    feature_vector = normalize_features(feature_vector)

    try:
        if hasattr(model, "predict_proba"):
            predictions = model.predict_proba(feature_vector.reshape(1, -1))
            label = int(np.argmax(predictions))
            confidence = float(np.max(predictions) * 100)
        else:
            predictions = model.predict(feature_vector.reshape(1, -1), verbose=0)
            label = int(np.argmax(predictions))
            confidence = float(np.max(predictions) * 100)
    except Exception as e:
        print(f"Pose classification error: {e}")
        return "Unknown", 0.0

    pose_name = get_pose_name(label)
    return pose_name, confidence
