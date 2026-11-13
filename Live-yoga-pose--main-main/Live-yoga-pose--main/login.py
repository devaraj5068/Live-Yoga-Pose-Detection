import tkinter as tk
from tkinter import messagebox
from database import validate_user, init_db
from register import RegisterWindow
from dashboard import DashboardWindow


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Yoga Posture Evaluation - Login")
        self.root.geometry("460x520")
        self.root.configure(bg="#0b0c10")
        init_db()
        self.build_ui()

    def build_ui(self):
        title = tk.Label(self.root, text="Yoga Posture Evaluation", bg="#0b0c10", fg="#66fcf1", font=("Helvetica", 20, "bold"))
        title.pack(pady=30)

        form_frame = tk.Frame(self.root, bg="#1f2833")
        form_frame.pack(padx=30, pady=15, fill="both", expand=True)

        tk.Label(form_frame, text="Username", bg="#1f2833", fg="#c5c6c7", font=("Helvetica", 12)).pack(pady=(20, 5), anchor="w", padx=16)
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 12), bg="#c5c6c7", fg="#0b0c10")
        self.username_entry.pack(padx=16, fill="x")

        tk.Label(form_frame, text="Password", bg="#1f2833", fg="#c5c6c7", font=("Helvetica", 12)).pack(pady=(20, 5), anchor="w", padx=16)
        self.password_entry = tk.Entry(form_frame, font=("Helvetica", 12), bg="#c5c6c7", fg="#0b0c10", show="*")
        self.password_entry.pack(padx=16, fill="x")

        login_btn = tk.Button(form_frame, text="Login", command=self.login_user, bg="#45a29e", fg="#0b0c10", font=("Helvetica", 13, "bold"), relief="flat")
        login_btn.pack(pady=30, padx=16, fill="x")

        register_btn = tk.Button(form_frame, text="Create Account", command=self.open_register, bg="#66fcf1", fg="#0b0c10", font=("Helvetica", 12), relief="flat")
        register_btn.pack(pady=(0, 20), padx=16, fill="x")

        note = tk.Label(form_frame, text="Use exact username and password to login.", bg="#1f2833", fg="#c5c6c7", font=("Helvetica", 10))
        note.pack(pady=10)

    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation", "Please enter both username and password.")
            return

        if validate_user(username, password):
            self.root.withdraw()
            DashboardWindow(self.root, username)
        else:
            messagebox.showerror("Authentication Failed", "Username or password is incorrect.")

    def open_register(self):
        RegisterWindow(self.root)
