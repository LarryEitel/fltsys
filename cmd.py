#import wingdbstub
from django.conf import settings
settings.configure()

from boundaries.models import Boundary

b = Boundary.objects.all()[0]

print b