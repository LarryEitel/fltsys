from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
#    url(r"^$", direct_to_template, {
#        "template": "homepage.html",
#    }, name="home"),
    url(r"^$", "participation.views.home", name="home"),

    url(r"^station-areas/$", "participation.views.station_areas_list", name="station_areas_list"),
    url(r"^station-areas/(?P<slug>[-\w]+)/$", "participation.views.station_area_detail", name="station_area_detail"),

    url(r"^getstation/$", "participation.views.get_nearest_station", name="get_nearest_station"),
    
    url(r"^themes/$", "participation.views.themes_list", name="themes_list"),
    url(r"^themes/(?P<slug>[-\w]+)/$", "participation.views.theme_detail", name="theme_detail"),
    
    url(r"^ideas/(?P<id>\d+)/$", "participation.views.idea_detail", name="idea_detail"),
    url(r"^meetingnotes/(?P<id>\d+)/$", "participation.views.meetingnote_detail", name="meetingnote_detail"),
    url(r"^newsarticles/(?P<id>\d+)/$", "participation.views.newsarticle_detail", name="newsarticle_detail"),
    url(r"^media/(?P<id>\d+)/$", "participation.views.media_detail", name="media_detail"),
    url(r"^data/(?P<id>\d+)/$", "participation.views.data_detail", name="data_detail"),
    
    url(r"^share/$", "participation.views.share", name="share"),
    url(r"^share/add/(?P<itemtype>[-\w]+)$", "participation.views.add_shareditem", name="add_shareditem"),
    url(r"^map/$", "participation.views.map_page", name="map_page"),
    url(r"^map/items/$", "participation.views.get_map_page_items", name="get_map_page_items"),

    url(r"^rate/item/(?P<id>\d+)$", "participation.views.rate_item", name="rate_item"),

    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^pages/", include("meta.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/", include("idios.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    url(r'^comments/', include('django.contrib.comments.urls')),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )


# serve media (uploads) on dev server
if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('', (r'^%s(?P<path>.*)$' % _media_url, serve, {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)
