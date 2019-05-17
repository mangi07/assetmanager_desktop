import tkinter as tk
from .asset_list import AssetButton, AssetRow
from .menu import AssetMenu


def init_widgets(parent):
    # define positioning here with Options objects
    
    asset_button_options = {"text":"Hello", "fg":"red"}
    parent.asset_button = AssetButton(asset_button_options)
    
    parent.master.menu = AssetMenu(parent.master)
    
    parent.asset_row = AssetRow(parent.master)
    

