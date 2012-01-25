import re
import sys
import simplejson as json
import cPickle as pickle

JSONDIR = '../private/json/'
PKLDIR = '../private/pkl/'
KMLDIR = '../private/kml/'


import numpy as np
import matplotlib.nxutils as nx
from matplotlib.nxutils import pnpoly



jsonfilename = JSONDIR + 'house_points.json'
json_data = open(jsonfilename).read()

old_house_pts = json.loads(json_data)

blocks = pickle.load( open( PKLDIR + "blocks2.pkl", "rb" ) )

house_pts = []

# for each block
for block in blocks:
    # get polygon points
    polygon = np.array([[pt[0], pt[1]] for pt in block['pts']], float)
    
    house_pt = {}
    
    # for each block, check lat lng to see if it exists in polygon
    for old_house_pt in old_house_pts:
        if nx.pnpoly( old_house_pt['lat'], old_house_pt['lng'], polygon):
            house_pt['district'] = block['district']
            house_pt['barrio'] = block['barrio']
            house_pt['blockno'] = block['no']
            house_pt['pt'] = [old_house_pt['lat'], old_house_pt['lng']]
            house_pts.append(house_pt)
    

pickle.dump( house_pts, open( PKLDIR + "house_pts.pkl", "wb" ) )
