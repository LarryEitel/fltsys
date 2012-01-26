from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from meta.models import Page

def get_page(request, slug):

	page = get_object_or_404(Page.objects, slug=slug)

	return render_to_response("meta/page.html", locals(), context_instance=RequestContext(request))
