#import wingdbstub
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import logging
from clevernote import CleverNote

logger_debug = logging.getLogger('logview.debug')

def index(request, *args, **kwargs):
    #print request.GET
    logger_debug.debug(request.META['QUERY_STRING'])
    return HttpResponse('')


def PostEn(request, userId, guid, reason, *args, **kwargs):
    template_name = "en/post.hamlpy"
    
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
    template_name = "en/base.hamlpy"
        