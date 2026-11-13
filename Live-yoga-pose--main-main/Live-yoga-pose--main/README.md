# AI Based Yoga Posture Evaluation System

## Overview
A complete Python-based final year / mini project that evaluates yoga poses in real time using webcam input. The system uses MediaPipe for pose landmark detection, OpenCV for webcam video capture, TensorFlow for pose classification, SQLite for user and session data storage, and Tkinter for a modern GUI.

## Features
- User authentication with login and registration
- Attractive dashboard interface
- Real-time yoga pose detection and skeleton drawing
- Support for Tree Pose, Cobra Pose, Warrior Pose, Triangle Pose, and Mountain Pose
- Posture accuracy scoring and corrective feedback
- Voice feedback using `pyttsx3`
- Progress tracking with session history
- Report generation with total sessions, best accuracy, average score, and history

## Folder Structure
```
AI_Yoga_Posture_Evaluation/
│── main.py
│── login.py
│── register.py
│── dashboard.py
│── yoga_detection.py
│── pose_classifier.py
│── feedback.py
│── database.py
│── train_model.py
│── reports.py
│── requirements.txt
│── model/
│     └── yoga_model.h5
│── database/
│     └── yoga.db
│── assets/
│     └── images/
│── README.md
```

## Setup Instructions
1. Open VS Code in the `AI_Yoga_Posture_Evaluation` folder.
2. Use Python 3.11 or 3.12 for best compatibility with TensorFlow and MediaPipe.
3. Create a Python virtual environment if desired:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
   If TensorFlow fails to install on your Python version, the project will still run using the scikit-learn fallback model.
5. Run the application:
   ```powershell
   python main.py
   ```

## Using the Project
1. The app opens the login screen.
2. Register a new account if needed.
3. Log in with your username and password.
4. Use the dashboard to start yoga evaluation.
5. The webcam opens and detects your pose.
6. Accuracy and feedback are displayed live.
7. Session history is saved automatically.
8. Open Reports to review progress.

## Model Training
The application automatically creates and saves a simple pose classification model to `model/yoga_model.h5` if it is missing. To retrain manually:
```powershell
python train_model.py
```

## Database Schema
- `users` table:
  - `id` INTEGER PRIMARY KEY
  - `username` TEXT UNIQUE
  - `password` TEXT
  - `created_at` TEXT
- `sessions` table:
  - `id` INTEGER PRIMARY KEY
  - `username` TEXT
  - `date` TEXT
  - `pose_name` TEXT
  - `accuracy` REAL
  - `duration_seconds` INTEGER
  - `feedback` TEXT

## Notes
- Press `q` or `Esc` to stop the yoga evaluation session.
- Make sure your webcam is connected and allowed for access.
- The system works best in a well-lit room with your full body visible.
