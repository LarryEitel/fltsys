from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def home(request):
	""" Homepage """
	return render_to_response("home/base.html", locals(), context_instance=RequestContext(request))
