#import wingdbstub
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import logging
from clevernote import CleverNote
from models import ENNote

logger_debug = logging.getLogger('logview.debug')

def get_enpts():
    enpts = ENNote.objects.filter(geocoded = True)
    return enpts


def index(request, *args, **kwargs):
    #print request.GET
    logger_debug.debug('en.views.index ' + request.META['QUERY_STRING'])
    return HttpResponse('')

def post(request, *args, **kwargs):
    MODFUNC = 'en.views.post'
    #print request.GET
    #logger_debug.debug(request.META['QUERY_STRING'])
    # http://x/evernote/?userId=123456&guid=523b72b2-71a6-4c14-bedd-30f2558ea72f&reason=update
    # http://x/evernote/post/?userid=53&guid=523b72b2-71a6-4c14-bedd-30f2558ea72f&reason=update
    try:
        userid = request.GET['userId']
        guid = request.GET['guid']
        reason = request.GET['reason']
    except:
        logger_debug.error("en.views.post GET params failed: " + request.META['QUERY_STRING'])
        return HttpResponse('')
    
    
    from models import ENNote
    import datetime
    from clevernote import CleverNote
    
    cn = CleverNote()
    
    withContent = True
    withResourcesData = False
    withResourcesRecognition = False
    withResourcesAlternateData = False
    
    note = cn.noteStore.getNote(cn.authToken, guid, withContent, withResourcesData, withResourcesRecognition, withResourcesAlternateData)
    
    
    try:
        en = ENNote.objects.get(guid=note.guid)
        logger_debug.debug("%s %s: %s %s" % (MODFUNC, "UPDATE", en.guid, en.title))
    except:
        en = ENNote()    
        logger_debug.debug("%s %s: %s %s" % (MODFUNC, "NEW", en.guid, en.title))
         
        
    cn.notebookName = "Territory POIs"        
    en.UpdateFromEN(note, cn) 
    
    return HttpResponse()

class HomeView(TemplateView):
    template_name = "en/base.hamlpy"
        