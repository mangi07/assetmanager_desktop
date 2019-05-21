import tkinter as tk
from PIL import Image, ImageTk
from models import models


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


class AssetRow(tk.LabelFrame):
    """
    Accepts asset with properties:
    asset_id (and others in Asset model)
    pics a list of Picture objects
    counts a list of LocationCount objects
    """
    def __init__(self, parent, asset):
        super().__init__(parent, bd=5, bg="#8caef2", text="Asset", padx=5, pady=5)
        self.grid()
        
        # ###############################
        id = tk.StringVar()
        id.set(asset.asset_id)
        
        description = tk.StringVar()
        description.set(asset.description)

        img_path = tk.StringVar()
        img_path.set(asset.pics[0].filepath)
        img_path2 = tk.StringVar()
        img_path2.set(asset.pics[1].filepath)
        # ##################################
        self.row = 0
        self.col = 0
        self.colors = ("#7c8eb2", "#bac2d3") # alternate column colors
        self.color_index = 0
        self.imgs = []

        self.add_field(id, "Asset ID")
        self.add_field(description, "Description")
        self.add_imgs([img_path, img_path2])
        

    def add_field(self, val, label_text):
        frame = tk.Frame(self, bd=5, bg=self.colors[self.color_index%2])
        frame.grid(row=self.row, column=self.col)
        label = tk.Label(frame, text=label_text)
        label.grid(row=0, column=0)
        field = tk.Label(frame, textvariable = val)
        field.grid(row=1, column=0)
        self.col += 1
        self.color_index += 1

    def add_imgs(self, paths):
        frame = tk.Frame(self, bd=5, bg=self.colors[self.color_index%2])
        frame.grid(row=self.row, column=self.col)
        
        label = tk.Label(frame, text="Images")
        label.grid(row=0, column=0)

        self.init_imgs(paths)
        label = tk.Label(frame, image=self.imgs[0])
        label.image = self.imgs[0]
        label.grid(row=1, column=0)
        
        self.col += 1
        self.color_index += 1

    def init_imgs(self, paths):
        for img in paths:
            i = Image.open(paths[0].get())
            i.thumbnail((50,50), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(i)
            self.imgs.append(render)