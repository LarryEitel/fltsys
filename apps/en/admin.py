from django.contrib import admin

from models import ENNote

class ENNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    list_filter = ('author', 'enupdated', 'geocoded')
    ordering = ('author', 'title')    

admin.site.register(ENNote, ENNoteAdmin)
