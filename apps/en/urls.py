from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
    url(r'^$', post, name="post"),
    
    # having trouble matching this url pattern
    url(r'^post', post, name="post"),
    #url(r"evernote/\?userId=(?P<userId>\d+)&guid=(?P<guid>.*?)&reason=(?P<reason>update|create)", "en.views.post", name="post"),    
    
)
