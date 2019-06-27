# ######################################################
# File: simplegui.py
# Description: app main entry point
#
# Run with 
#   python -m app.views.simplegui
# from project root directory 'app' folder 


import PySimpleGUI as sg
from datetime import datetime
import re
from ..models import models
from ..controllers.asset_controller import AssetController



# #########################################################
# View-related items

#sg.ChangeLookAndFeel('Dark')
sg.ChangeLookAndFeel('Topanga')
BACKGROUND_COLOR = 'black'
TEXT_COLOR = 'yellow'


date_format = 'yyyy-mm-dd hh:mm:ss'
money_format = '####.##'
default_bulk_count = 1
asset_controller = AssetController()

# ##########################################################################################
# Window layouts
# ##########################################################################################

# ##################################################
# Add New Asset: TODO
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

def update_view():
	window.FindElement('view_description').Update('new text')

# ##################################################
# Asset Listing, Filtering, and Editing: TODO: refactor into a class or separate module
AVP = ['view_id_','view_description_'] # Asset View Prefix
AEP = ['input_id_', 'input_description_'] # Asset Edit Prefix

def get_asset_view_layout():
	prev_results_len = 0
	assets = asset_controller.getAssets(prev_results_len)
	'''
	[
		(1, '0', 'Split AC, Carrier - FLC Generator 3 Control Room', 1, None, None, 
		'Assets - Air Conditioning, Split Ductless', None, 'HCA', '38KCE009118/', None, 1, 
		'2009-01-01 00:00:00', None, '2019-05-14 06:03:59', None, 'Carrier', None, 7000000000000, 
		None, None, 8, None, '"Some fields estimated. 9000 BTU (9K)"', 1), ...
	]
	'''
	rows = []
	for i in range(0,5):
		layout = [
			[sg.Text('ID: '), sg.Text(' '*30, key=AVP[0]+str(i)), sg.InputText(' '*10, key=AEP[0]+str(i), visible=False)],
			[sg.Text('Description: '), sg.Text(' '*30, key=AVP[1]+str(i)), sg.InputText(' '*10, key=AEP[1]+str(i), visible=False)],
			[sg.Text('Test: '), sg.Multiline('', disabled=True, key=f'view_description3{i}')],
			[sg.Button(f'Edit({i})'), sg.Button(f'Update({i})', visible=False)],
		]
		frame = sg.Frame(title=None, layout=layout)
		rows.append([frame])
	rows.append([sg.Button('Get Assets'),])
	#print(rows)
	layout = [sg.Column(layout=rows, scrollable=True)]
	return [layout]

asset_input_event = re.compile('Edit\((\d+)\)')
asset_update_event = re.compile('Update\((\d+)\)')

def asset_input_action(event, window):
	result = asset_input_event.match(event)
	if result:
		i = result.group(1) # The id of the frame showing the asset
		# set all inputs and update button visible (and hide Edit button on successful operation?)
		for x in range(0,2):
			window.Element(AVP[x]+i).Update(visible=False)
			window.Element(AEP[x]+i).Update(visible=True)
		window.Element(f'Update({i})').Update(visible=True)
		window.Element(f'Edit({i})').Update(visible=False)

def asset_update_action(event, window, values):
	result = asset_update_event.match(event)
	if result:
		i = result.group(1)
		for x in range(0,2):
			window.Element(AVP[x]+i).Update(visible=True)
			window.Element(AEP[x]+i).Update(visible=False)
			# TODO: update values of sg.Text elements with entries from sg.InputText elements
		# TODO: actually grab inputs and update database
		window.Element(f'Update({i})').Update(visible=False)
		window.Element(f'Edit({i})').Update(visible=True)			




# #################################################
# Navigation Menu
menu_def = [
	['Navigation', ['Exit']],
]  
menu = [sg.Menu(menu_def, )]


# #################################################
# Tabs Setup
tab1 = get_asset_input_layout()
tab2 = get_asset_view_layout()
tabs = [sg.TabGroup([[sg.Tab('Tab 1', tab1), sg.Tab('Tab 2', tab2)]], tooltip='TIP2')]


# ##################################################
# GUI Initialization
window = sg.Window('Asset Management', [menu + tabs])
event, values = window.Read()
add_asset_default_values = values


# ###########################################################################
# GUI event loop
while True:
	#event, values = windows[curr_window].Read()
	event, values = window.Read()
	print(event)
	if event is None or event == 'Exit':
		break
	if event == 'Add Asset':
		try:
			#print("\n\nField values from form:")
			#print(values)
			asset_controller.addAsset(values)
		except Exception as e:
			sg.Popup('Input Error: ', e)
	if event == 'Clear Form':
		window.Fill(add_asset_default_values)

	if event == 'Get Assets':
		update_view()

	asset_input_action(event, window)
	asset_update_action(event, window, values)

