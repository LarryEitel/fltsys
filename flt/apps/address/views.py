#import wingdbstub
from django.shortcuts import render_to_response
from django.conf import settings
import flt.apps.common.views
import flt.apps.address.models

def coffee(request):
    return render_to_response('address/coffee.html', {'STATIC_URL': settings.STATIC_URL})
	
class AsyncContactView(flt.apps.common.views.BackboneView):
    model = flt.apps.address.models.ContactModel
    url_root = "async/contact"