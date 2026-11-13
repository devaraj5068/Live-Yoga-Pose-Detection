import os
import sqlite3
from sqlite3 import Error
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "yoga.db")

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

CREATE_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    date TEXT NOT NULL,
    pose_name TEXT NOT NULL,
    accuracy REAL NOT NULL,
    duration_seconds INTEGER NOT NULL,
    feedback TEXT,
    FOREIGN KEY(username) REFERENCES users(username)
);
"""


def create_connection():
    try:
        os.makedirs(DB_DIR, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        return conn
    except Error as e:
        print(f"SQLite connection error: {e}")
        return None


def init_db():
    conn = create_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_SESSIONS_TABLE)
        conn.commit()
    except Error as e:
        print(f"SQLite init error: {e}")
    finally:
        conn.close()


def add_user(username, password):
    conn = create_connection()
    if conn is None:
        return False, "Database connection failed"
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
            (username, password, datetime.now().isoformat()),
        )
        conn.commit()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Error as e:
        return False, str(e)
    finally:
        conn.close()


def validate_user(username, password):
    conn = create_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT password FROM users WHERE username = ?", (username,)
        )
        row = cursor.fetchone()
        if row and row[0] == password:
            return True
        return False
    except Error as e:
        print(f"Validate user error: {e}")
        return False
    finally:
        conn.close()


def add_session(username, pose_name, accuracy, duration_seconds, feedback):
    conn = create_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (username, date, pose_name, accuracy, duration_seconds, feedback) VALUES (?, ?, ?, ?, ?, ?)",
            (
                username,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                pose_name,
                accuracy,
                duration_seconds,
                feedback,
            ),
        )
        conn.commit()
        return True
    except Error as e:
        print(f"Add session error: {e}")
        return False
    finally:
        conn.close()


def fetch_user_sessions(username):
    conn = create_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT date, pose_name, accuracy, duration_seconds, feedback FROM sessions WHERE username = ? ORDER BY id DESC",
            (username,),
        )
        return cursor.fetchall()
    except Error as e:
        print(f"Fetch sessions error: {e}")
        return []
    finally:
        conn.close()


def fetch_report_summary(username):
    conn = create_connection()
    if conn is None:
        return {
            "total_sessions": 0,
            "best_accuracy": 0,
            "average_accuracy": 0,
        }
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*), MAX(accuracy), AVG(accuracy) FROM sessions WHERE username = ?",
            (username,),
        )
        row = cursor.fetchone()
        total = row[0] or 0
        best = float(row[1]) if row[1] is not None else 0.0
        avg = float(row[2]) if row[2] is not None else 0.0
        return {
            "total_sessions": total,
            "best_accuracy": round(best, 2),
            "average_accuracy": round(avg, 2),
        }
    except Error as e:
        print(f"Report summary error: {e}")
        return {
            "total_sessions": 0,
            "best_accuracy": 0,
            "average_accuracy": 0,
        }
    finally:
        conn.close()
