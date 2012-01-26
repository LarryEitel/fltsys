from django.contrib import admin
from meta.models import Page

class PageAdmin(admin.ModelAdmin):
	list_display = ("title", "order")
	search_fields = ("title", "content",)
	prepopulated_fields = { "slug": ("title",) }
	
admin.site.register(Page, PageAdmin)