from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase

class Profile(ProfileBase):
	name = models.CharField(_("My name"), max_length=50, null=True, blank=True)
	about = models.TextField(_("About me"), null=True, blank=True)
	#website = models.URLField(_("My website"), null=True, blank=True, verify_exists=False)
