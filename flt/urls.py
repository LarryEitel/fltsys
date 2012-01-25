from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from django.views.generic import TemplateView

from flt.apps.address.views import AsyncContactView
from flt.apps.address.views import coffee

admin.autodiscover()

urlpatterns = patterns('',
    url(r"^$", include('flt.apps.home.urls')),
    url(r"evernote/", include('flt.apps.en.urls')),
    url(AsyncContactView.make_url(), AsyncContactView.as_view(), name='async_contact_view'),
    url(r'contacts/coffee', coffee, name="coffee"),
    url(r'contacts', TemplateView.as_view(template_name="address/contact.html"), name="contact_view"),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('flt.apps.accounts.urls')),
)

urlpatterns += staticfiles_urlpatterns()
