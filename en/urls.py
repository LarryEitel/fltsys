from django.conf.urls.defaults import patterns, include, url

from views import *

urlpatterns = patterns('',
    #url(r'userId=(?P<userId>\d+)/$', PostEn, name="PostEn"),
    url(r'userId=(?P<userId>\d+)[&\?]guid=(?P<guid>.*?)[&\?]reason=(?P<reason>update|create)/$', PostEn, name="PostEn"),
    #url(r'^userId=(?P<userId>\d+)/$', PostEn, name="PostEn"),
    #url(r'userId=42$', PostEn, name="PostEn"),
    #url(r'^$', PostEn, name="PostEn"),
    url(r'^$', HomeView.as_view(), name="index"),
)
