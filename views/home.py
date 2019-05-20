import tkinter as tk
from .mwidgets import init_widgets


class HomeWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid()
        self.master = master
        self.master.title("Asset Management")
        
        init_widgets(self)

def init():
    root = tk.Tk()
    root.geometry("400x300")
    app = HomeWindow(master=root)
    app.mainloop()