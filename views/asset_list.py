import tkinter as tk


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
        self.grid()
    
    # when ready, refactor out and pass in method to bind in __init__
    def temp_method(self):
        print("Testing")


class AssetRow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
        
        # refactor into controller
        v = tk.StringVar()
        v.set("testing tk variable")
        
        self.asset_id = tk.Label(self, textvariable = v)
        self.asset_id.grid()
