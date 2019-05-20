import tkinter as tk
from PIL import Image, ImageTk


class AssetMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        
        parent.config(menu=self)
        self.parent = parent
        
        menus = [
            ("File", [
                ("Exit", self.client_exit),
            ]),
            ("Edit", [
                ("Undo", None),
                ("Show Image", self.showImg),
                ("Show Text", self.showText),
            ])
        ]
        for heading, items in menus:
            self._create_menu(heading, items)


    def _create_menu(self, heading, items):
        menu = tk.Menu(self)
        for label, command in items:
            menu.add_command(label=label, command=command)
        self.add_cascade(label=heading, menu=menu)
    
    # refactor out?
    def client_exit(self):
        exit()
    
    # refactor into view and controller
    def showImg(self):
        load = Image.open("media/truck.jpg")
        render = ImageTk.PhotoImage(load)

        img = tk.Label(self.parent, image=render)
        img.image = render
        img.grid()

    # refactor into view and controller
    def showText(self):
        text = tk.Label(self.parent, text="Just an example.")
        text.grid()