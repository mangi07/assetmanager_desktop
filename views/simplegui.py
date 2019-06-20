# ######################################################
# File: simplegui.py
# Description: app main entry point
#
# Run with 
#   python -m app.views.simplegui
# from project root directory 'app' folder 


import PySimpleGUI as sg
from datetime import datetime
from ..models import models
from ..controllers.asset_controller import AssetController



# #########################################################
# View-related items

#sg.ChangeLookAndFeel('Dark')
sg.ChangeLookAndFeel('Topanga')
"""
asset_view_layout = [      
          [sg.Text('Asset Listing')],

          [sg.Text(f'ID: {asset.asset_id}'), 
          	sg.Text(f'Description: {asset.description}'),
          ],      
          [sg.Text('Address', size=(15, 1)), sg.InputText('')],      
          [sg.Text('Phone', size=(15, 1)), sg.InputText('')],      
          [sg.Submit(), sg.Cancel()]      
         ]
"""

date_format = 'yyyy-mm-dd hh:mm:ss'
money_format = '####.##'
default_bulk_count = 1
asset_controller = AssetController()
ADD_ASSET_WINDOW = 1
VIEW_ASSETS_WINDOW = 2

# #######################################################
# Window layouts

def get_asset_input_layout():
	return [
		# identification
		[sg.Text('ID: '), sg.InputText('', key='id'),],
		[sg.Text('Description: '), sg.InputText('', key='description'),],
		[sg.Text('Current: '), sg.Checkbox('(not retired/disposed)', default=True, key='current'),],
		[sg.Text('Model #: '), sg.InputText('', key='model'), sg.Text('Serial #: '), sg.InputText('', key='serial'),],

		# money stuff
		[sg.Text('Cost: ', tooltip=money_format), sg.InputText('', key='cost')],
		[sg.Text('Shipping Cost: ', tooltip=money_format), sg.InputText('', key='shipping')],
		[sg.Text('Cost Brand New: ', tooltip=money_format), sg.InputText('', key='cost_brand_new')],
		[sg.Text('Life Expectancy: '), sg.Spin([i for i in range(1,40)], initial_value=1, key='life_expectancy'), sg.Text('years'),],

		# dates
		[sg.Text(f'Date Placed: ', tooltip=date_format), sg.InputText(datetime.now(), key='date_placed'), 
			sg.CalendarButton(button_text='change date', target=(sg.ThisRow, -1)),],
		[sg.Text('Date Removed: ', tooltip=date_format), sg.InputText(key='date_removed'), 
			sg.CalendarButton(button_text='change date', target=(sg.ThisRow, -1)),],
		[sg.Text('Date Warranty Expires: ', tooltip=date_format), sg.InputText(key='date_warranty_expires'), 
			sg.CalendarButton(button_text='change date', target=(sg.ThisRow, -1)),],

		# locations and counts
		[sg.Text('Bulk Count: '), sg.Text(str(default_bulk_count), key='bulk_count'),],

		[sg.Text('Notes'), sg.Multiline('', key='notes'),],
		[sg.Checkbox('Entered in MaintenanceDirect', default=False, key='maint_dir'),],


		[sg.Button('Add Asset'), sg.Button('Clear Form')]
	]

def get_asset_view_layout():
	
	return [
		[sg.Text('Test'),],
	]


# #################################################
# Navigation Menu
menu_def = [
	['Navigation', ['Exit']],
]  
menu = [sg.Menu(menu_def, )]


# #################################################
# Window Management
def get_window_layout(win_type):
	if win_type == ADD_ASSET_WINDOW:
		return get_asset_input_layout()
	elif win_type == VIEW_ASSETS_WINDOW:
		return get_asset_view_layout()
	else:
		return get_asset_input_layout()

tab1 = get_window_layout(ADD_ASSET_WINDOW)
tab2 = get_window_layout(VIEW_ASSETS_WINDOW)
tabs = [sg.TabGroup([[sg.Tab('Tab 1', tab1), sg.Tab('Tab 2', tab2)]], tooltip='TIP2')]
#window.Layout(menu + tabs)


# ##################################################
# GUI Initialization
print([menu + tabs])
window = sg.Window('Asset Management', [menu + tabs])
event, values = window.Read()
add_asset_default_values = values

# ###########################################################################
# GUI event loop

# TODO: probably need to go back to tabbed layout
while True:
	#event, values = windows[curr_window].Read()
	event, values = window.Read()
	print(event)
	if event is None or event == 'Exit':
		break
	if event == 'Add Asset':
		try:
			print("\n\nField values from form:")
			print(values)
			asset_controller.addAsset(values)
		except Exception as e:
			sg.Popup('Input Error: ', e)
	if event == 'Clear Form':
		window.Fill(add_asset_default_values)