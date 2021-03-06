# ###################################################################
# File: insert_sql.py
# Created: 4/29/2019
#
# Description: main entry point and runner for the other scripts in this folder
# ###################################################################

import load_excel as imports
import locations_import
import models
import sqlite3



def insert_message(table, statement):
    print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~~~~~~inserting into {}...\n\n".format(table) + statement)


def list_to_column_names(mlist):
    return str(mlist).replace("'",'').replace("[",'').replace("]",'')


def insert_from_lists(mlists, column_names, mtable, mcursor):
    columns_str = list_to_column_names(column_names)
    
    params = "(" + ''.join( ["?, "]*(len(mlists[0])-1) ) + "?)"
    insert = "INSERT INTO {} ({}) VALUES {}".format(mtable, columns_str, params)
    vals = [tuple(vals_list) for vals_list in mlists]
    
    #insert_message(mtable, str(vals))
    cursor.executemany(insert, vals);
    conn.commit()


def set_ids(items_list):
    index = 1
    for item in items_list:
        item.id = index
        index += 1


def insert_items(table_name, items, clazz, cursor):
    if False in [isinstance(i, int) for i in items]:
        set_ids(items)
    mlists = [item.list_vals() for item in items]
    for i, mlist in enumerate(mlists):
        mlists[i] = [None if x=="nan" else x for x in mlist]
    column_names = clazz.list_column_names()
    insert_from_lists(mlists, column_names, table_name, cursor)


conn = sqlite3.connect('assetsdb.sqlite3')
cursor = conn.cursor()


insert_items("manufacturer", imports.manufacturers.values(), models.Manufacturer, cursor)
insert_items("supplier", imports.suppliers.values(), models.Supplier, cursor)
insert_items("category", imports.categories.values(), models.Category, cursor)
insert_items("department", imports.departments.values(), models.Department, cursor)
insert_items("purchase_order", imports.purchase_orders.values(), models.PurchaseOrder, cursor)



#####################################################################################
# now we can insert assets that have foreign keys to the items we just inserted above

def get_fk(field, lookup):
    if field is not None and field != "nan" and field in lookup:
        id = lookup[field].id
        assert(isinstance(id, int))
        return id
    else:
        return None

# set foreign keys
assets_list = imports.assets.values()
for asset in assets_list:
    # requisition
    if asset.requisition == "awaiting invoice":
        asset.requisition = 1
    elif asset.requisition == "partial payment":
        asset.requisition = 2
    elif asset.requisition == "paid in full":
        asset.requisition = 3
    elif asset.requisition == "donated":
        asset.requisition = 4
    else:
        asset.requisition = None
    # receiving
    if asset.receiving == "shipped":
        asset.receiving = 1
    elif asset.receiving == "received":
        asset.receiving = 2
    elif asset.receiving == "placed":
        asset.receiving = 3
    else:
        asset.receiving = None
    # setting foreign keys for the remaining asset fields
    asset.po_number = get_fk(asset.po_number, imports.purchase_orders)
    asset.asset_class1 = get_fk(asset.asset_class1, imports.categories)
    asset.asset_class2 = get_fk(asset.asset_class1, imports.categories)
    asset.manufacturer = get_fk(asset.manufacturer, imports.manufacturers)
    asset.supplier = get_fk(asset.supplier, imports.suppliers)
    asset.department = get_fk(asset.department, imports.departments)
    
    assert(isinstance(asset.po_number, int) or asset.po_number is None)
    assert(isinstance(asset.asset_class1, int) or asset.asset_class1 is None)
    assert(isinstance(asset.asset_class2, int) or asset.asset_class2 is None)
    assert(isinstance(asset.manufacturer, int) or asset.manufacturer is None)
    assert(isinstance(asset.supplier, int) or asset.supplier is None)
    assert(isinstance(asset.department, int) or asset.department is None)
    

insert_items("asset", imports.assets.values(), models.Asset, cursor)



##########################################################################################################
# now that we have assets inserted, we can insert rows involving m2m relationships in the remaining tables
# Overview:
#
# account
# far
# invoice
# picture
# location
#
# asset_far
# asset_invoice
# asset_picture
# location_count


# FAR
insert_items("account", imports.accounts.values(), models.Account, cursor)
for far in imports.fars.values():
    far.account = far.account.id
    assert(isinstance(far.account, int))
insert_items("far", imports.fars.values(), models.Far, cursor)
# asset_fars # TODO
for af in imports.asset_fars:
    af.asset = af.asset.id
    af.far = af.far.id
insert_items("asset_far", imports.asset_fars, models.AssetFar, cursor)

# location counts
for loc in imports.locations:
    assert(loc.id is not None)
insert_items("location", imports.locations, models.Location, cursor)
for loc_count in imports.location_counts:
    loc_count.asset = loc_count.asset.id
    loc_count.location = loc_count.location.id
    assert(loc_count.location is not None)
insert_items("location_count", imports.location_counts, models.LocationCount, cursor)

# TEST #########################################################
# invoices
insert_items("invoice", imports.invoices.values(), models.Invoice, cursor)
for ai in imports.asset_invoices:
    ai.asset = ai.asset.id
    ai.invoice = ai.invoice.id
insert_items("asset_invoice", imports.asset_invoices, models.AssetInvoice, cursor)

# TEST #########################################################
# asset pictures
insert_items("picture", imports.pictures.values(), models.Picture, cursor)
for ap in imports.asset_pics:
    ap.asset = ap.asset.id
    ap.filepath = ap.filepath.id
insert_items("asset_picture", imports.asset_pics, models.AssetPicture, cursor)


conn.close()


# TEST asset-far associations
#for af in asset_fars:
#    print(af)

# TEST asset-picture associations
#for ap in asset_pics:
#    print(ap)

# TEST asset-invoice associations
#for ai in asset_invoices:
#    print(ai)


"""
asset_fars = [] # TODO
invoices = {}
asset_invoices = []
root_location
"""


