import tkinter as tk
from tkinter import messagebox
from database import add_user


class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register - AI Yoga Posture Evaluation")
        self.geometry("420x440")
        self.configure(bg="#0b0c10")
        self.build_ui()

    def build_ui(self):
        title = tk.Label(self, text="Create New Account", bg="#0b0c10", fg="#66fcf1", font=("Helvetica", 18, "bold"))
        title.pack(pady=24)

        frame = tk.Frame(self, bg="#1f2833")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        tk.Label(frame, text="Username", bg="#1f2833", fg="#c5c6c7", font=("Helvetica", 12)).pack(pady=(20, 5), anchor="w", padx=16)
        self.username_entry = tk.Entry(frame, font=("Helvetica", 12), bg="#c5c6c7", fg="#0b0c10")
        self.username_entry.pack(padx=16, fill="x")

        tk.Label(frame, text="Password", bg="#1f2833", fg="#c5c6c7", font=("Helvetica", 12)).pack(pady=(20, 5), anchor="w", padx=16)
        self.password_entry = tk.Entry(frame, font=("Helvetica", 12), bg="#c5c6c7", fg="#0b0c10", show="*")
        self.password_entry.pack(padx=16, fill="x")

        tk.Label(frame, text="Confirm Password", bg="#1f2833", fg="#c5c6c7", font=("Helvetica", 12)).pack(pady=(20, 5), anchor="w", padx=16)
        self.confirm_entry = tk.Entry(frame, font=("Helvetica", 12), bg="#c5c6c7", fg="#0b0c10", show="*")
        self.confirm_entry.pack(padx=16, fill="x")

        register_btn = tk.Button(frame, text="Register", command=self.register_user, bg="#66fcf1", fg="#0b0c10", font=("Helvetica", 13, "bold"), relief="flat")
        register_btn.pack(pady=28, padx=16, fill="x")

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not username or not password or not confirm:
            messagebox.showwarning("Validation", "Please fill in all fields.")
            return

        if password != confirm:
            messagebox.showwarning("Validation", "Passwords do not match.")
            return

        success, message = add_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
            self.destroy()
        else:
            messagebox.showerror("Error", message)
