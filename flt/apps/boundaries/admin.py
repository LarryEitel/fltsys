from django.contrib.gis import admin
from olwidget.admin import GeoModelAdmin
from flt.apps.boundaries.models import Boundary, BoundaryType, BoundariesRelated

# Customize the map
class BoundaryAdmin(GeoModelAdmin):
    options = {
        'layers': ['google.streets', 'google.hybrid'],
    }
    list_map = ['poly']
    
    
class BoundaryTypeAdmin(admin.ModelAdmin):
    pass

class BoundariesRelatedAdmin(admin.ModelAdmin):
    pass

admin.site.register(Boundary, BoundaryAdmin)
admin.site.register(BoundaryType, BoundaryTypeAdmin)
admin.site.register(BoundariesRelated, BoundariesRelatedAdmin)

