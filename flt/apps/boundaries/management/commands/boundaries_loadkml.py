#import wingdbstub
from django.core.management.base import BaseCommand, CommandError
import sys
import os
#sys.path.append("../..")
import settings
from boundaries.models import Boundary, BoundaryType, BoundariesRelated
# Import XML parser
from xml.dom.minidom import parseString

class Command(BaseCommand):
    help = 'Load KML of boundaries/polygons'

    def handle(self, *args, **options):
        filename = os.path.join(settings.KMLDIR, "territory_boundaries.kml")
        
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