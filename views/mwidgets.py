import tkinter as tk
from .asset_list import AssetButton, AssetRow
from .menu import AssetMenu
from .models import models


def init_widgets(parent):
    # define positioning here with Options objects
    
    asset_button_options = {"text":"Hello", "fg":"red"}
    parent.asset_button = AssetButton(asset_button_options)
    
    parent.menu = AssetMenu(parent.master)
    
    # ###########################
    # refactor to obtain the following from sql queries
    asset = Asset()
    asset.asset_id = "dummy_asset1"
    
    pic1 = models.Picture()
    pic1.id = 1
    pic1.filepath = "media/truck.jpg"
    pic2 = models.Picture()
    pic2.id = 2
    pic2.filepath = "media/logo.png"
    asset_pics = [pic1, pic2]
    
    # Add locations before this point so recursive __str__ works on Location obj
    # sql query for all locations
    loc_count1 = models.LocationCount() # obtain from sql
    loc1 = 
    loc_count1.location = loc1 # obtain this object by id from in-memory location objs
    loc_count1.count = 5
    loc_count1.audit_date = None # date last audited
    counts = [loc_count1]
    # ###########################
    asset.pics = asset_pics
    asset.counts = counts
    parent.asset_row = models.AssetRow(parent.master, asset) # tag on pics and counts as properties
    

