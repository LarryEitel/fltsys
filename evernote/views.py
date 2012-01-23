import wingdbstub
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext

def PostEn(request, userId, guid, reason, *args, **kwargs):
    template_name = "evernote/post.hamlpy"
    
    context = {
        "userId": userId,
        "guid": guid,
        "reason": reason,
    }    
        
    return render_to_response(
        template_name,
        RequestContext(request, context)
    )


class HomeView(TemplateView):
    template_name = "evernote/base.hamlpy"
        