from django import template

from meta.models import Page

register = template.Library()

def page_links(placement):
	""" 
	Returns a list with links to all available meta pages.
	Used as footer for instance.
	"""
	
	pages = Page.objects.filter(placement=placement)
	
	return {
		'pages': pages,
	}

register.inclusion_tag("meta/_page_links.html")(page_links)