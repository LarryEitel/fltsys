import os
from django.contrib.gis.utils import LayerMapping
from participation.models import Station, Line

station_mapping = {
	'name' : 'NAME', 
	'geometry' : 'POINT',
}
station_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/stations_4326.shp'))

def stations(verbose=True):
	lm = LayerMapping(Station, station_shp, station_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)
	
line_mapping = {
	'geometry' : 'LINESTRING',
}
line_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/line_4326.shp'))

def lines(verbose=True):
	lm = LayerMapping(Line, line_shp, line_mapping, transform=False, encoding='iso-8859-1')
	lm.save(strict=True, verbose=verbose)