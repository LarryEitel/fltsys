#import wingdbstub
import re
import sys
import cPickle as pickle
import simplejson as json

JSONDIR = '../private/json/'
PKLDIR = '../private/pkl/'
KMLDIR = '../private/kml/'

# territory boundaries
xml = open(KMLDIR + 'territory_boundaries.kml').read()
items = re.findall("<coordinates>(.*?)</coordinates>", xml)
boundaries = []
for item in items:
    pts = re.findall(r"(?P<latlong>.*?,.*?),0\.00 ", item)
    boundaries.append(pts)
    
pickle.dump( boundaries, open( PKLDIR + "territories.pkl", "wb" ) )   

sys.exit()





# block_numbers
xml = open(KMLDIR + 'block_layer.kml').read()
reobj = re.compile("<coordinates>(?P<coords>.*?)</coordinates>", re.MULTILINE)
blocks = []
for match in reobj.finditer(xml):
    block = {}
    ptsstring = re.findall(r"(?P<latlong>.*?,.*?),0\.00 ", match.group('coords'))
    
    pts = []
    for ptstring in ptsstring:
        latlng = [float(n) for n in ptstring.split(',')]
        ll = {}
        ll['lat'] = latlng[0]
        ll['lng'] = latlng[1]
        #print ll
        pts.append(ll)
        
    block['pts'] = pts
    blocks.append(block)

        

jsonfilename = JSONDIR + 'blocks.json'
fh = open(jsonfilename, 'wb')
fh.write(json.dumps(blocks).encode('utf-8'))
fh.close()
	
sys.exit()

reobj = re.compile(r"TEXT\s+1\s+(?:(?P<province>\d)-(?P<district>\d+)-(?P<barrio>\d+)-00-(?P<block>\d+))*\s*\d+\s+Block Labels Full\s+10\s+(?P<lat>.*?)\s+20\s+(?P<lng>.*?)\s+40.*?(?=TEXT|$)", re.DOTALL)





# parse out block polygons
xml = open(KMLDIR + 'block_labels.dxf').read()


reobj = re.compile(r"TEXT\s+1\s+(?:(?P<province>\d)-(?P<district>\d+)-(?P<barrio>\d+)-00-(?P<block>\d+))*\s*\d+\s+Block Labels Full\s+10\s+(?P<lat>.*?)\s+20\s+(?P<lng>.*?)\s+40.*?(?=TEXT|$)", re.DOTALL)

reobj = re.compile(r"TEXT\s+1\s+(?:(?P<province>\d)-(?P<district>\d+)-(?P<barrio>\d+)-00-(?P<block>\d+))*\s*\d+\s+Block Labels Full\s+10\s+(?P<lat>.*?)\s+20\s+(?P<lng>.*?)\s+40.*?(?=TEXT|$)", re.DOTALL)

block_numbers = []
for match in reobj.finditer(xml):
    province = match.group('province')
    if not province:
        continue
    
    district = int(match.group('district'))
    barrio = int(match.group('barrio'))
    block = int(match.group('block'))
    lat = float(match.group('lat'))
    lng = float(match.group('lng'))
    
    print province, district, barrio, block, lat, lng
    
    block_numbers.append({"district": district, "barrio": barrio, "block": block, "lat": lat, "lng": lng})

jsonfilename = JSONDIR + 'block_numbers.json'
fh = open(jsonfilename, 'wb')
fh.write(json.dumps(block_numbers).encode('utf-8'))
fh.close()
	


# territory boundaries
xml = open('block_layer.kml').read()
items = re.findall("<coordinates>(.*?)</coordinates>", xml)
boundaries = []
for item in items:c
    
terr['block_layer'] = block_layer









terr = {}

## territory boundaries
#xml = open('Territory Boundaries.xml').read()
#items = re.findall("<coordinates>(.*?)</coordinates>", xml)
#boundaries = []
#for item in items:
    #pts = re.findall(r"(?P<latlong>.*?,.*?),0\.00 ", item)
    #boundaries.append(pts)
    
#terr['boundaries'] = boundaries



## district boundaries
#xml = open('Distrito.xml').read()
#items = re.findall("<coordinates>(.*?)</coordinates>", xml)
#districts = []
#for item in items:
    #pts = re.findall(r"(?P<latlong>.*?,.*?),0\.00 ", item)
    #districts.append(pts)
    
#terr['districts'] = districts

## landmarks
#xml = open('Landmark.xml').read()
#items = re.findall("<coordinates>(.*?)</coordinates>", xml)
#landmarks = []
#for item in items:
    #pts = re.findall(r"(?P<latlong>.*?,.*?),0\.00 ", item)
    #landmarks.append(pts)
    
#terr['landmarks'] = landmarks


# homes
xml = open(KMLDIR + 'house_points_layer.kml').read()
items = re.findall("<coordinates>(.*?)</coordinates>", xml)
housepoints = []

reobj = re.compile(r"(?P<lng>.*?),(?P<lat>.*?),0\.00 ", re.DOTALL)
for item in items:
    match = reobj.search(item)
    if not match:
        raise ValueError("Failed to find lat lng")
    lat = float(match.group("lat"))
    lng = float(match.group("lng"))
    
    housepoints.append({"lat": lat, "lng": lng, "title": ''})

jsonfilename = JSONDIR + 'house_points.json'
fh = open(jsonfilename, 'wb')
fh.write(json.dumps(housepoints).encode('utf-8'))
fh.close()
		

## waitingrooms
#xml = open('WaitingRooms.xml').read()
#items = re.findall("<coordinates>(.*?)</coordinates>", xml)
#waitingrooms = []
#for item in items:
    #pts = re.findall(r"(?P<latlong>.*?,.*?),0\.00 ", item)
    #waitingrooms.append(pts)
    
#terr['waitingrooms'] = waitingrooms

#print terr
