import tkinter as tk
from database import init_db
from login import LoginWindow
from train_model import train_and_save
import os


def prepare_environment():
    init_db()
    if not os.path.exists("model/yoga_model.h5"):
        train_and_save()


def main():
    prepare_environment()
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
