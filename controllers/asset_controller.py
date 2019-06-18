from ..models import models
import sqlite3


class AssetController:
    def addAsset(self, fields):
        asset = self._makeAsset(**fields)
        asset_lists = [asset.list_vals()]

        conn, cursor = _open_db()

        insert = _insert_from_lists(asset_lists, asset.list_column_names(), 'asset', cursor, conn)




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
        
        # Add locations before this point so recursive __str__ works on Location obj
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
        return int(s) * 10000000000

    def _makeAsset(self, id, description, current, model, serial, 
        date_placed, date_removed, date_created, date_warranty_expires,
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
        asset.date_record_created = date_created
        asset.date_warranty_expires = date_warranty_expires
        asset.cost = cost # TODO: change
        asset.shipping = shipping # TODO: change
        asset.cost_brand_new = cost_brand_new # TODO: change
        asset.life_expectancy_years = life_expectancy
        asset.notes = notes
        asset.maint_dir = maint_dir
        asset.bulk_count = 1

        return asset

def _open_db():
    conn = sqlite3.connect('./app/assetsdb.sqlite3')
    cursor = conn.cursor()
    return conn, cursor

def _list_to_column_names(mlist):
    return str(mlist).replace("'",'').replace("[",'').replace("]",'')

# maybe adapt some of this code...
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