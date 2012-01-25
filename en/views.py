import wingdbstub
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

def post(request, *args, **kwargs):
    #print request.GET
    logger_debug.debug(request.META['QUERY_STRING'])
    # http://x/evernote/post/?userid=53&guid=523b72b2-71a6-4c14-bedd-30f2558ea72f&reason=update
    try:
        userid = request.GET['userid']
        guid = request.GET['guid']
        reason = request.GET['reason']
        logger_debug.debug("en.views.post GET params succeeded: " + request.META['QUERY_STRING'])
    except:
        logger_debug.debug("en.views.post GET params failed: " + request.META['QUERY_STRING'])
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
        logger_debug.debug("en.views.post update: " + en.guid + ' ' + en.title)        
    except:
        en = ENNote()    
        logger_debug.debug("en.views.post new: " + en.guid + ' ' + en.title) 
        
        
    cn.notebookName = "Territory POIs"        
    en.Update(note, cn) 
    
    return HttpResponse('', status=200)


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
        