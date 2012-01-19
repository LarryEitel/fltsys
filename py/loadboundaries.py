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
        
        # example: 
        # INSERT INTO flt_boundaries_test SET boundary = (GeomFromText('POLYGON((-84.145393330458063 9.9789556383996896, -84.143642183664099 9.9717359981087821, -84.136791205856127 9.96863308887737, -84.135255112177205 9.9712137262579503, -84.135777384028046 9.9717667199823605, -84.135808105901617 9.9722889918331923, -84.133811184119025 9.9734257011555911, -84.13510150280932 9.9770816041114117, -84.13249014355516 9.982949481964873, -84.132643752923045 9.9830109257120299, -84.134087680981239 9.9817206070217388, -84.136944815224012 9.9815055539066915, -84.137958637052108 9.9811061695501735, -84.138450187029349 9.9827344288498239, -84.14060071817984 9.9834103100685478, -84.141675983755079 9.9819356601367879, -84.145393330458063 9.9789556383996896))'))

        cursor.execute(sql)
        x = 0

LoadTable(PKLDIR + 'territories.pkl', FLT_BOUNDARIES)

