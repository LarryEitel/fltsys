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



#jsonfilename = JSONDIR + 'block_numbers.json'
#json_data = open(jsonfilename).read()

#block_numbers = json.loads(json_data)
#blocks = [block for block in block_numbers]


#jsonfilename = JSONDIR + 'block_polygons_sample.json'
#jsonfilename = JSONDIR + 'block_polygons.json'
#json_data = open(jsonfilename).read()
#blocks_polygons = json.loads(json_data)

#new_blocks = []

## for each block polygon
#for block_polygon in blocks_polygons:
    ## get polygon points
    #polygon = np.array([[pt['lat'], pt['lng']] for pt in block_polygon['pts']], float)
    
    ## for each block, check lat lng to see if it exists in polygon
    #for block in blocks:
        #if nx.pnpoly( block['lat'], block['lng'], polygon):
            #block['pts'] = block_polygon['pts']
            #new_blocks.append(block)
    

#pickle.dump( new_blocks, open( PKLDIR + "blocks.pkl", "wb" ) )


blocks = pickle.load( open( PKLDIR + "blocks.pkl", "rb" ) )

new_blocks = []

for block in blocks:
    new_block = {}
    new_block['district'] = block['district']
    new_block['barrio'] = block['barrio']
    new_block['no'] = block['block']
    new_block['label_pt'] = [block['lng'], block['lat']]
    new_block['pts'] = [[pt['lng'], pt['lat']] for pt in block['pts']]
    new_blocks.append(new_block)

pickle.dump( new_blocks, open( PKLDIR + "blocks2.pkl", "wb" ) )
