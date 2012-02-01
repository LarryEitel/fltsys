#import wingdbstub
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Boundary

import gpolyencode

def get_polys():
    """ Query Boundary and return encoded polygons optimized for Google Maps. """

    #from boundaries.models import Boundary
    #p = polys = Boundary.objects.filter(boundary_type = 5)[0]
    #print p.poly.geojson

    congregations = Boundary.objects.filter(boundary_type = 4).exclude(poly__isnull=True)
    territories = Boundary.objects.filter(boundary_type = 5).exclude(poly__isnull=True)

    # encode
    encoder = gpolyencode.GPolyEncoder()

    for poly in congregations: poly.encoded = encoder.encode(poly.coords[0])
    for poly in territories: poly.encoded = encoder.encode(poly.coords[0])


    polys = {
        'congregations': congregations,
        'territories': territories,
    }


    return polys


def home(request):
    """ Homepage """
    return render_to_response("home/base.html", locals(), context_instance=RequestContext(request))

def map_page(request):
    """Create the explore map page"""
    #stations = Station.objects.all()
    #lines = get_greenline()

    #themes = Theme.objects.all()

    #itemtypes = Shareditem.ITEMTYPES

    return render_to_response("home/map.html", locals(), context_instance=RequestContext(request))
