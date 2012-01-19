import wingdbstub
from django.core.management.base import BaseCommand, CommandError
import sys
import os
import settings
from boundaries.models import Boundary, BoundaryType, BoundariesRelated

class Command(BaseCommand):
    help = 'Boundary Test'

    def handle(self, *args, **options):
        print "Start"
        
        center_pt = bs[600].center_pt
        bscontains = Boundary.objects.exclude(boundary_type__id=5).filter(poly__contains=center_pt)
        
        print "\nFinished!"