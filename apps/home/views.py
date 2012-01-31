from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from boundaries.views import get_polys

def home(request):
	""" Homepage """
	polys = get_polys()
	context = {
	        'polys' : polys,
	        }
	return render_to_response("home/base.html", locals(), context_instance=RequestContext(request, context))

def map_page(request):
	"""Create the explore map page"""
	#stations = Station.objects.all()
	#lines = get_greenline()
	
	#themes = Theme.objects.all()
	
	#itemtypes = Shareditem.ITEMTYPES
	
	return render_to_response("home/map.html", locals(), context_instance=RequestContext(request))
	