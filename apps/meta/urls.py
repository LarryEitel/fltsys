from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^(?P<slug>[-\w]+)/$", "meta.views.get_page", name="meta_page"),
    # url(r"^terms/$", direct_to_template, {"template": "about/terms.html"}, name="terms"),
    # url(r"^privacy/$", direct_to_template, {"template": "about/privacy.html"}, name="privacy"),
    # url(r"^dmca/$", direct_to_template, {"template": "about/dmca.html"}, name="dmca"),
    # url(r"^what_next/$", direct_to_template, {"template": "about/what_next.html"}, name="what_next"),
)
