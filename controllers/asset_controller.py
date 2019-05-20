from ..models import models
import sqlite3


class AssetController:
    _index = 0
    
    _asset_list = []
    
    def _get_batch:
        # TODO: populate from sql query
        a1 = models.Asset()
        a1.asset_id = "test_asset_1"
        a1.description = "Test Asset 1"
        
        a2 = models.Asset()
        a2.asset_id = "test_asset_2"
        a2.description = "Test Asset 2"
        
        _asset_list.extend([a1,a2])
    
    def has_next:
        
    def get_next:
        if len(_asset_list) <= _index
        
    def get_pics_with_id(asset_id):
        # TODO: make list from sql query to get pic paths from asset id
        return ["media/truck.jpg"]

# maybe adapt some of this code...
def insert_from_lists(mlists, column_names, mtable, mcursor):
    columns_str = list_to_column_names(column_names)
    
    params = "(" + ''.join( ["?, "]*(len(mlists[0])-1) ) + "?)"
    insert = "INSERT INTO {} ({}) VALUES {}".format(mtable, columns_str, params)
    vals = [tuple(vals_list) for vals_list in mlists]
    
    #insert_message(mtable, str(vals))
    cursor.executemany(insert, vals);
    conn.commit()