from django.conf.urls.defaults import patterns, url

from home.views import HomeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="index"),
)
