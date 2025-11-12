import tkinter as tk
from gui.gui_config import GUI


if __name__ == "__main__":
    window = tk.Tk()
    app = GUI(window)
    window.mainloop()