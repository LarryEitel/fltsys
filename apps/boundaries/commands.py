# https://github.com/zacharyvoase/django-boss
# http://docs.python.org/dev/library/argparse.html
from djboss.commands import *
# a copy of this file should be copied to djboss app dir
import wingdbstub

@command
def boundarytypes(args):
    from boundaries.models import BoundaryType
    for bt in BoundaryType.objects.all().order_by('name'):
        print bt.name + ' - ' + bt.title + ':', bt.id
        
    
    
@command
@argument('kmlfilename', help="kml filename only")
@argument('boundary_type_id', type=int, help="Boundary Type ID")
def kml(args):
    """Load boundary polygons from a KML."""
    
    import sys
    import os
    
    from boundaries.models import Boundary, BoundaryType, BoundariesRelated
    from xml.dom.minidom import parseString    
    import settings
    
    #b = Boundary.objects.all()[0]
    file_path = os.path.join(settings.KMLDIR, args.kmlfilename)
    boundary_type_id = args.boundary_type_id
    
    # file exists?
    if not os.path.exists(file_path):
        print "File not found: %s" % file_path
        sys.exit()
    
    # boundary_type id valid?
    try:
        boundary_type_id = BoundaryType.objects.get(id=boundary_type_id).id
    except:
        print  "Invalid Boundary Type ID: %d" % boundary_type_id
        sys.exit()
    
    print file_path, boundary_type_id
    
    # Parse kml_str
    kml = parseString(open(file_path).read())
    added = 0
    failed = 0
    
    print "Loading boundaries from: %s" % file_path
    
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
        b.boundary_type_id = boundary_type_id
        b.save()
    
    print "\nFinished!"
    print "Successfully added: %d" % added
    if failed:
        print "Failed to add: %d" % failed    