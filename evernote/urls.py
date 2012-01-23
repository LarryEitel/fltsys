from django.conf.urls.defaults import patterns, url

from views import HomeView, PostEn


urlpatterns = patterns('views',
    #url(r'userId=(?P<userId>\d+)/$', PostEn, name="PostEn"),
    url(r'userId=(?P<userId>\d+)[&\?]guid=(?P<guid>.*?)[&\?]reason=(?P<reason>update|create)/$', PostEn, name="PostEn"),
    #url(r'^userId=(?P<userId>\d+)/$', PostEn, name="PostEn"),
    #url(r'userId=42$', PostEn, name="PostEn"),
    #url(r'^$', PostEn, name="PostEn"),
    url(r'^$', HomeView.as_view(), name="index"),
)
