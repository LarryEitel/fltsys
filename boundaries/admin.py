from boundaries.models import Boundary, BoundaryType, BoundariesRelated
from django.contrib import admin

class BoundaryAdmin(admin.ModelAdmin):
    pass

class BoundaryTypeAdmin(admin.ModelAdmin):
    pass

class BoundariesRelatedAdmin(admin.ModelAdmin):
    pass

admin.site.register(Boundary, BoundaryAdmin)
admin.site.register(BoundaryType, BoundaryTypeAdmin)
admin.site.register(BoundariesRelated, BoundariesRelatedAdmin)
