#import wingdbstub
import re
import sys
sys.path.append("../") 
import cPickle as pickle
import simplejson as json
import MySQLdb as mdb
import local_settings

JSONDIR = '../private/json/'
PKLDIR = '../private/pkl/'
KMLDIR = '../private/kml/'

FLT_BOUNDARIES = 'flt_boundaries_test'

# INSERT INTO flt_boundaries_test VALUSE 'PolygonFromText(POLYGON(0 0,10 0,10 10,0 10,0 0))'

def LoadTable(filename, tblname):
    
    dat = pickle.load(open(filename, 'rb'))
    db = local_settings.DATABASES['default']
    conn = mdb.connect(db['HOST'], db['USER'], db['PASSWORD'], db['NAME'])   
    
    cursor = conn.cursor(mdb.cursors.DictCursor)  
    
    for boundary in dat:
        # Generate as string of points to be used in insert
        # '(-84.145393330458063 9.9789556383996896, -84.143642183664099 9.9717359981087821, ...)'
        pts_string = str(tuple([ll.replace(',',' ') for ll in boundary])).replace("'","")
        sql = "INSERT INTO %s SET boundary = (GeomFromText('POLYGON(%s)'))" % (FLT_BOUNDARIES, pts_string)
        cursor.execute(sql)
        x = 0

LoadTable(PKLDIR + 'territories.pkl', FLT_BOUNDARIES)

