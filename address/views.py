from django.shortcuts import render_to_response
from django.conf import settings
import common.views
import address.models

def coffee(request):
    return render_to_response('address/coffee.html', {'STATIC_URL': settings.STATIC_URL})
	
class AsyncContactView(common.views.BackboneView):
    model = address.models.ContactModel
    url_root = "async/contact"