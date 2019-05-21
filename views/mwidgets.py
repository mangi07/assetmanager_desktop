import tkinter as tk
from .asset_list import AssetButton, AssetRow
from .menu import AssetMenu
from models import models
from controllers.asset_controller import AssetController


def init_widgets(parent):
    # define positioning here with Options objects

    asset_controller = AssetController()
    asset = asset_controller.getAsset()
    parent.asset_row = AssetRow(parent.master, asset) # tag on pics and counts as properties
    parent.asset_row = AssetRow(parent.master, asset)

