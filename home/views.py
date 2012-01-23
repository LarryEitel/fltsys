#if 'c:' in __file__: import wingdbstub
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.shortcuts import render_to_response


class HomeView(TemplateView):

    template_name = "home/base.hamlpy"
