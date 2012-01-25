from django.contrib.gis import admin
from flt.apps.olwidget.admin import GeoModelAdmin
from flt.apps.world.models import WorldBorder

# Customize the map
class WorldBorderAdmin(GeoModelAdmin):
    options = {
        'layers': ['google.streets', 'google.hybrid'],
    }
    list_map = ['mpoly']
    
admin.site.register(WorldBorder, WorldBorderAdmin)