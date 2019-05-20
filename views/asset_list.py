import tkinter as tk
from PIL import Image, ImageTk
from .models import model


class AssetButton(tk.Button):
    """
    options: text, fg
    """
    def __init__(self, options):
        kwargs = {
            "text" : options["text"],
            "fg" : options["fg"],
            "command" : self.temp_method
        }
        super().__init__(**kwargs)
        self.grid(row=0, column=3)
    
    # when ready, refactor out and pass in method to bind in __init__
    def temp_method(self):
        print("Testing")


class AssetRow(tk.Frame):
    """
    Accepts asset with properties:
    asset_id (and others in Asset model)
    pics a list of Picture objects
    counts a list of LocationCount objects
    """
    def __init__(self, parent, asset):
        super().__init__(parent, bd=5, bg="yellow")
        self.grid()
        
        # ###############################
        # refactor into controller
        id = tk.StringVar()
        id.set(asset.asset_id)
        
        img_path = tk.StringVar()
        img_path.set("media/truck.jpg")
        # ##################################
        
        self.asset_id = tk.Label(self, textvariable = id)
        self.asset_id.grid(row=0)
        
        self.asset_id = tk.Label(self, textvariable = id)
        self.asset_id.grid(row=0, column=1)
        
        load = Image.open(img_path.get())
        render = ImageTk.PhotoImage(load)
        self.img = tk.Label(self, image=render)
        self.img.image = render
        self.img.grid(row=0, column=2)
