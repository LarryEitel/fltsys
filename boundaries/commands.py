# https://github.com/zacharyvoase/django-boss
from djboss.commands import *
import wingdbstub

@command
#@argument('app', type=APP_LABEL)
@argument('kmlfilename', help="kml filename only")
@argument('boundary_type_id', type=int, help="Boundary Type ID")
def kml(args):
    """Load KML."""
    
    import sys
    import os
    from boundaries.models import Boundary, BoundaryType, BoundariesRelated
    from xml.dom.minidom import parseString    
    import settings
    
    #b = Boundary.objects.all()[0]
    filename = os.path.join(settings.KMLDIR, args.kmlfilename)
    print filename, args.kmlfilename, args.boundary_type_id
    
    sys.exit()
    
    # Parse kml_str
    kml = parseString(open(filename).read())
    added = 0
    failed = 0
    
    print "Loading boundaries from: %s" % filename
    
    for placemark in kml.getElementsByTagName("Placemark"):
        polygon = placemark.getElementsByTagName("Polygon")
        try:
            kml_str = polygon[0].toxml()
            sys.stdout.write('.')
        except:
            sys.stdout.write('!')
            failed += 1
            continue
        
        added += 1
        b = Boundary()
        b.set_poly_from_kml_str(kml_str)
        b.boundary_type_id = 5
        b.save()
    
    print "\nFinished!"
    print "Successfully added: %d" % added
    print "Failed to add: %d" % failed    