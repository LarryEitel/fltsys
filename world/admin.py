from django.contrib.gis import admin
from olwidget.admin import GeoModelAdmin
from world.models import WorldBorder

# Customize the map
class WorldBorderAdmin(GeoModelAdmin):
    options = {
        'layers': ['google.streets'],
    }
    list_map = ['mpoly']
    
admin.site.register(WorldBorder, WorldBorderAdmin)