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

    def _convertCurrencyToDB(self, s):
        print("\nIn _convertCurrencyToDB, string:")
        print(s)
        return float(s) * self.currency_factor

    def _convertDBToCurrency(self, i):
        return str(i/self.currency_factor) if i is not '' and i is not None else 0

    def _get_fars(self, conn, id):
        select = '''
            select far.id as far_id, far.account as far_account, far.description as far_description, 
            far.pdf as far_pdf, far.life as far_life, far.start_date as far_start_date
            from asset
            left join asset_far on asset_far.asset = asset.id
            left join far on asset_far.far = far.id
            where asset.id = {}
            limit 1;
        '''.format(id)
        cursor = conn.execute(select)
        results = cursor.fetchall()
        fars = []
        for far in results:
            fars.append(
                {'far_id':far[0], 'far_account':far[1], 'far_description':far[2], 'far_pdf':far[3], 
                'far_life':far[4], 'far_start_date':far[5]}
            )
        return fars
    def _get_invoices(self, conn, id):
        select = '''
            select invoice.id, invoice.number, invoice.file_path
            from asset
            left join asset_invoice on asset_invoice.asset = asset.id
            left join invoice on asset_invoice.invoice = invoice.id
            where asset.id = {}
            limit 1;
        '''.format(id)
        cursor = conn.execute(select)
        results = cursor.fetchall()
        invoices = []
        for invoice in results:
            invoices.append(
                {'invoice_id':invoice[0], 'invoice_number':invoice[1], 'invoice_file_path':invoice[2]}
            )
        return invoices
    def _get_location_counts(self, conn, id):
        select = '''
            select location.id, location.description, count, audit_date
            from asset
            left join location_count on location_count.asset = asset.id
            left join location on location_count.location = location.id
            where asset.id = {}
            limit 1;
        '''.format(id)
        cursor = conn.execute(select)
        results = cursor.fetchall()
        location_counts = []
        for loc in results:
            location_counts.append(
                {'location_id':loc[0], 'location_description':loc[1], 'count':loc[2], 'audit_date':loc[3]}
            )
        return location_counts
    def _get_pic_paths(self, conn, id):
        select = '''
            select picture.file_path
            from asset
            left join asset_picture on asset_picture.asset = asset.id
            left join picture on asset_picture.picture = picture.id
            where asset.id = {}
            limit 1;
        '''.format(id)
        cursor = conn.execute(select)
        results = cursor.fetchall()
        pic_paths = []
        for pic_path in results:
            pic_paths.append(
                {'pic_path':pic_path[0]}
            )
        return pic_paths
    def _add_m2m(self, conn, asset):
        id = asset['id']
        fars = self._get_fars(conn, id)
        invoices = self._get_invoices(conn, id)
        location_counts = self._get_location_counts(conn, id)
        pic_paths = self._get_pic_paths(conn, id)
        asset['fars'] = fars
        asset['invoices'] = invoices
        asset['location_counts'] = location_counts
        asset['pictures'] = pic_paths
        return asset

    # TODO: add filtering functionality as a parameter, and use in select string to modify with where clauses
    def getAssets(self, getting_next=True):
        """
        getting_next determines pagination direction
        each new call returns the next page (eg: first 5, next 5, next 5...)
        if getting_next, page forwards, else page backwards ...by pagination delta
        """
        '''
            select asset.id, asset.asset_id, asset.description, asset.is_current, 
            requisition.status as requisition_status, receiving.status as receiving_status,
            cat_1.name as category_1, cat_2.name as category_2, department.name as department_name,
            asset.model_number, asset.serial_number, asset.bulk_count,
            asset.date_placed, asset.date_removed, asset.date_record_created, asset.date_warranty_expires,
            manufacturer.name as manufacturer_name, supplier.name as supplier_name,
            asset.cost, asset.shipping, asset.cost_brand_new, asset.life_expectancy_years,
            purchase_order.number as purchase_order_number,
            asset.notes, asset.maint_dir,

            far.id as far_id, far.account as far_account, far.description as far_description, 
            far.pdf as far_pdf, far.life as far_life, far.start_date as far_start_date,

            invoice.id as invoice_id, invoice.number as invoice_number, invoice.file_path as invoice_file_path,

            location.id as location_id, location.description as location_description, 
            location_count.count, location_count.audit_date, 

            picture.file_path as picture_file_path

            from asset

            left join requisition on asset.requisition = requisition.id
            left join receiving on asset.receiving = receiving.id
            left join category as cat_1 on asset.category_1 = cat_1.id
            left join category as cat_2 on asset.category_2 = cat_2.id
            left join manufacturer on asset.manufacturer = manufacturer.id
            left join supplier on asset.supplier = supplier.id
            left join purchase_order on asset.purchase_order = purchase_order.id
            left join department on asset.department = department.id

            left join asset_far on asset_far.asset = asset.id
            left join far on asset_far.far = far.id

            left join asset_invoice on asset_invoice.asset = asset.id
            left join invoice on asset_invoice.invoice = invoice.id

            left join location_count on location_count.asset = asset.id
            left join location on location_count.location = location.id

            left join asset_picture on asset_picture.asset = asset.id
            left join picture on asset_picture.picture = picture.id
        '''
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

        asset_keys = [
            'id', 'asset_id', 'description', 'is_current', 
            'requisition_status', 'receiving_status',
            'category_1', 'category_2', 'department_name',
            'model_number', 'serial_number', 'bulk_count',
            'date_placed', 'date_removed', 'date_record_created', 'date_warranty_expires',
            'manufacturer_name', 'supplier_name',
            'cost', 'shipping', 'cost_brand_new', 'life_expectancy_years',
            'purchase_order_number',
            'notes', 'maint_dir',

            'fars', 'invoices', 'location_counts', 'pictures'
        ]

        # TODO: use config to load db path
        #conn = sqlite3.connect('./app/assetsdb.sqlite3')
        conn = sqlite3.connect('./app/assetsdb_use_this.sqlite3')
        try:
            with conn:
                cursor = conn.execute(select)
                self.assets = cursor.fetchall()
                for index, asset in enumerate(self.assets):
                    asset = dict(zip(asset_keys, asset))
                    asset = self._add_m2m(conn, asset)
                    asset['view_cost'] = self._convertDBToCurrency(asset['cost'])
                    asset['view_shipping'] = self._convertDBToCurrency(asset['shipping'])
                    asset['view_cost_brand_new'] = self._convertDBToCurrency(asset['cost_brand_new'])
                    self.assets[index] = asset

        except Exception as e:
            print("In asset_controller.getAssets: ")
            print(e)
        conn.close()
        
        '''
        (1, '0', 'Split AC, Carrier - FLC Generator 3 Control Room', 1, None, None, 
        'Assets - Air Conditioning, Split Ductless', None, 'HCA', '38KCE009118/', None, 1, 
        '2009-01-01 00:00:00', None, '2019-05-14 06:03:59', None, 'Carrier', None, 7000000000000, 
        None, None, 8, None, '"Some fields estimated. 9000 BTU (9K)"', 1)
        '''
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