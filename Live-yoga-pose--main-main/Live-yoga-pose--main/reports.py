import tkinter as tk
from tkinter import ttk
from database import fetch_report_summary, fetch_user_sessions


class ReportWindow(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.title("Yoga Report")
        self.geometry("700x550")
        self.configure(bg="#1a1a2e")
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        summary = fetch_report_summary(self.username)

        header = tk.Label(self, text="Your Progress Report", bg="#1a1a2e", fg="#f5f6fa", font=("Helvetica", 18, "bold"))
        header.pack(pady=14)

        frame = tk.Frame(self, bg="#16213e")
        frame.pack(pady=10, padx=16, fill="x")

        for label_text, value in [
            ("Total Sessions", summary["total_sessions"]),
            ("Best Accuracy", f"{summary['best_accuracy']} %"),
            ("Average Accuracy", f"{summary['average_accuracy']} %"),
        ]:
            block = tk.Frame(frame, bg="#16213e")
            block.pack(side="left", expand=True, fill="both", padx=6, pady=10)
            tk.Label(block, text=label_text, bg="#16213e", fg="#a5c9ff", font=("Helvetica", 12, "bold")).pack(pady=6)
            tk.Label(block, text=value, bg="#16213e", fg="#f8f9fa", font=("Helvetica", 16, "bold")).pack(pady=8)

        history_label = tk.Label(self, text="Pose History", bg="#1a1a2e", fg="#f5f6fa", font=("Helvetica", 16, "bold"))
        history_label.pack(pady=10)

        columns = ("Date", "Pose", "Accuracy", "Duration", "Feedback")
        table = ttk.Treeview(self, columns=columns, show="headings", height=10)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=120, anchor="center")

        sessions = fetch_user_sessions(self.username)
        for session in sessions:
            table.insert("", tk.END, values=session)

        table.pack(padx=12, pady=8, fill="both", expand=True)

        close_btn = tk.Button(self, text="Close", command=self.destroy, bg="#0f3460", fg="#ffffff", font=("Helvetica", 12, "bold"), relief="flat")
        close_btn.pack(pady=12)
