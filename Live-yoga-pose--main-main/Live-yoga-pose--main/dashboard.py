import tkinter as tk
from tkinter import messagebox
from reports import ReportWindow
from yoga_detection import start_yoga_evaluation
from datetime import datetime


class DashboardWindow(tk.Toplevel):
    def __init__(self, root, username):
        super().__init__(root)
        self.root = root
        self.username = username
        self.title("Yoga Dashboard")
        self.geometry("760x520")
        self.configure(bg="#0b0c10")
        self.build_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_ui(self):
        welcome = tk.Label(self, text=f"Welcome, {self.username}", bg="#0b0c10", fg="#66fcf1", font=("Helvetica", 22, "bold"))
        welcome.pack(pady=24)

        desc = tk.Label(self, text="Monitor your yoga posture and improve every session.", bg="#0b0c10", fg="#c5c6c7", font=("Helvetica", 13))
        desc.pack(pady=(0, 28))

        button_frame = tk.Frame(self, bg="#0b0c10")
        button_frame.pack(padx=20, pady=10, fill="both", expand=True)

        btn_specs = [
            ("Start Yoga Evaluation", self.launch_yoga, "#45a29e"),
            ("View Reports", self.open_reports, "#c5c6c7"),
            ("Exercise Guide", self.open_guide, "#66fcf1"),
            ("Exit", self.on_close, "#1f2833"),
        ]

        for text, command, color in btn_specs:
            button = tk.Button(button_frame, text=text, command=command, bg=color, fg="#0b0c10", font=("Helvetica", 14, "bold"), relief="flat")
            button.pack(pady=14, ipadx=12, ipady=10, fill="x")

        guide_label = tk.Label(self, text="Supported Poses: Mountain, Tree, Warrior, Triangle, Cobra", bg="#0b0c10", fg="#c5c6c7", font=("Helvetica", 11, "italic"))
        guide_label.pack(pady=8)

    def launch_yoga(self):
        self.withdraw()
        try:
            start_yoga_evaluation(self.username)
        except Exception as e:
            messagebox.showerror("Evaluation Error", f"Failed to start yoga evaluation:\n{e}")
        finally:
            self.deiconify()

    def open_reports(self):
        ReportWindow(self, self.username)

    def open_guide(self):
        message = (
            "Yoga Exercise Guide:\n\n"
            "- Mountain: Stand tall with feet together.\n"
            "- Tree: Place one foot on inner thigh and balance.\n"
            "- Warrior: Widen stance, bend front knee.\n"
            "- Triangle: Stretch to the side and keep arms aligned.\n"
            "- Cobra: Lie on belly and lift chest with arms."
        )
        messagebox.showinfo("Exercise Guide", message)

    def on_close(self):
        self.root.destroy()
