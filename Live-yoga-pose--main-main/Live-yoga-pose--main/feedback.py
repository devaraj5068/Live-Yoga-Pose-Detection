import pyttsx3


class FeedbackEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        try:
            self.engine.setProperty("rate", 165)
            self.engine.setProperty("volume", 1.0)
        except Exception:
            pass

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            print("Voice feedback is unavailable.")


def generate_feedback(pose_name, angles):
    feedback = []

    if pose_name == "Tree Pose":
        if angles.get("left_knee_angle", 180) > 160 and angles.get("right_knee_angle", 180) > 160:
            feedback.append("Bend one knee and place foot on inner thigh")
        if angles.get("left_hip_angle", 180) > 170 and angles.get("right_hip_angle", 180) > 170:
            feedback.append("Keep your hips squared and balanced")
        if angles.get("left_shoulder_angle", 180) < 120 or angles.get("right_shoulder_angle", 180) < 120:
            feedback.append("Raise your arms upward for balance")
    elif pose_name == "Cobra Pose":
        if angles.get("shoulder_hip_angle", 0) < 70:
            feedback.append("Lift your chest higher")
        if angles.get("back_angle", 180) > 160:
            feedback.append("Arch your back gently")
    elif pose_name == "Warrior Pose":
        if angles.get("front_knee_angle", 180) > 95:
            feedback.append("Bend the front knee more deeply")
        if angles.get("back_leg_angle", 180) < 160:
            feedback.append("Straighten the back leg")
    elif pose_name == "Triangle Pose":
        if angles.get("side_tilt_angle", 180) > 35:
            feedback.append("Reach your top arm higher")
        if angles.get("back_straightness", 0) < 150:
            feedback.append("Keep your spine straighter")
    elif pose_name == "Mountain Pose":
        if angles.get("left_shoulder_angle", 180) < 160 or angles.get("right_shoulder_angle", 180) < 160:
            feedback.append("Relax your shoulders and widen your stance")
        if angles.get("back_angle", 180) < 170:
            feedback.append("Keep your back straight")

    if not feedback:
        feedback.append("Good posture")

    return feedback
