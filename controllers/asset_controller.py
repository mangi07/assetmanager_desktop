from ..models import models
from .paginator import Paginator
import sqlite3


class AssetController:
    def __init__(self):
        self.currency_factor = 10000000000
        self.MAX_PAGE_SIZE = 5
        self.paginator = Paginator(self.MAX_PAGE_SIZE)
        self.assets = []

    def addAsset(self, fields):
        asset = self._makeAsset(**fields)
        asset_lists = [asset.list_vals()]

        conn, cursor = _open_db()

        insert = _insert_from_lists(asset_lists, asset.list_column_names(), 'asset', cursor, conn)

    def getAssets(self, getting_next=True):
        """
        getting_next determines pagination direction
        each new call returns the next page (eg: first 5, next 5, next 5...)
        if getting_next, page forwards, else page backwards ...by pagination delta
        """
        limit, offset = self.paginator.getPagination(len(self.assets), getting_next)
        select = '''
            select asset.id, asset.asset_id, asset.description, asset.is_current, 
            requisition.status as requisition_status, receiving.status as receiving_status,
            cat_1.name as category_1, cat_2.name as category_2, department.name as department_name,
            asset.model_number, asset.serial_number, asset.bulk_count,
            asset.date_placed, asset.date_removed, asset.date_record_created, asset.date_warranty_expires,
            manufacturer.name as manufacturer_name, supplier.name as supplier_name,
            asset.cost, asset.shipping, asset.cost_brand_new, asset.life_expectancy_years,
            purchase_order.number as purchase_order_number,
            asset.notes, asset.maint_dir
            from asset
            left join requisition on asset.requisition = requisition.id
            left join receiving on asset.receiving = receiving.id
            left join category as cat_1 on asset.category_1 = cat_1.id
            left join category as cat_2 on asset.category_2 = cat_2.id
            left join manufacturer on asset.manufacturer = manufacturer.id
            left join supplier on asset.supplier = supplier.id
            left join purchase_order on asset.purchase_order = purchase_order.id
            left join department on asset.department = department.id
            limit {} offset {};
        '''.format(limit, offset)

        selectM2M = None # TODO

        # TODO: use config to load db path
        #conn = sqlite3.connect('./app/assetsdb.sqlite3')
        conn = sqlite3.connect('./app/assetsdb_use_this.sqlite3')
        try:
            with conn:
                cursor = conn.execute(select)
                self.assets = cursor.fetchall()
        except Exception as e:
            print("In asset_controller.getAsset: ")
            print(e)
        conn.close()
        
        print(self.assets)
        return self.assets


    def getAsset(self):
        # ###########################
        # refactor to obtain the following from sql queries
        asset = models.Asset()
        asset.asset_id = "dummy_asset1"
        asset.description = "a;sdfkja;sdgha;sdjf;asdjf;asdfja;ljdfal;sdfja;sldjfa;sjgoiwnfasd;jf;salfj"
        
        pic1 = models.Picture()
        pic1.id = 1
        pic1.filepath = "media/truck.jpg"
        pic2 = models.Picture()
        pic2.id = 2
        pic2.filepath = "media/logo.png"
        asset_pics = [pic1, pic2]
        
        # TODO: Add locations before this point so recursive __str__ works on Location obj
        # sql query for all locations
        loc_count1 = models.LocationCount() # obtain from sql
        
        loc1 = models.Location()
        loc1.id = 1
        loc1.description = "test description"
        
        loc_count1.location = loc1 # obtain this object by id from in-memory location objs
        loc_count1.count = 5
        loc_count1.audit_date = None # date last audited
        counts = [loc_count1]
        # ###########################
        asset.pics = asset_pics
        asset.counts = counts

        return asset

    def _convertCurrencyToDB(self, s):
        print("\nIn _convertCurrencyToDB, string:")
        print(s)
        return float(s) * self.currency_factor

    # TODO: try out - may or may not work as expected
    def _convertDBToCurrency(self, i):
        return str(i/self.currency_factor) if i is not '' else 0

    def _makeAsset(self, id, description, current, model, serial, 
        date_placed, date_removed, date_warranty_expires,
        cost, shipping, cost_brand_new, life_expectancy, 
        notes, maint_dir):

        asset = models.Asset()
        asset.asset_id = id
        asset.description = description
        asset.is_current = current
        asset.model_number = model
        asset.serial_number = serial
        asset.date_placed = date_placed
        asset.date_removed = date_removed
        asset.date_warranty_expires = date_warranty_expires
        asset.cost = self._convertCurrencyToDB(cost)
        asset.shipping = self._convertCurrencyToDB(shipping)
        asset.cost_brand_new = self._convertCurrencyToDB(cost_brand_new)
        asset.life_expectancy_years = life_expectancy
        asset.notes = notes
        asset.maint_dir = maint_dir
        asset.bulk_count = 1

        return asset

# ##################################################################################
# TODO: refactor these out to some DB utility module ?

def _open_db():
    conn = sqlite3.connect('./app/assetsdb.sqlite3')
    cursor = conn.cursor()
    return conn, cursor

def _list_to_column_names(mlist):
    return str(mlist).replace("'",'').replace("[",'').replace("]",'')

def _insert_from_lists(mlists, column_names, mtable, mcursor, mconn):
    print(mlists[0])
    columns_str = _list_to_column_names(column_names)
    
    params = "(" + ''.join( ["?, "]*(len(mlists[0])-1) ) + "?)"
    insert = "INSERT INTO {} ({}) VALUES {}".format(mtable, columns_str, params)
    print(insert)
    vals = [tuple(vals_list) for vals_list in mlists]
    
    mcursor.executemany(insert, vals);
    mconn.commit()

    mconn.close()