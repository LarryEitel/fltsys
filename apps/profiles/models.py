from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase
from participation.models import Station, Shareditem


class Profile(ProfileBase):
	name = models.CharField(_("My name"), max_length=50, null=True, blank=True)
	about = models.TextField(_("About me"), null=True, blank=True)
	website = models.URLField(_("My website"), null=True, blank=True, verify_exists=False)
	mystation = models.ForeignKey(Station, verbose_name="My Station", null=True, blank=True)
	flickr_id = models.CharField("My Flickr account", max_length=50, null=True, blank=True)
	youtube_id = models.CharField("My YouTube account", max_length=50, null=True, blank=True)
	twitter_id = models.CharField("My Twitter account", max_length=50, null=True, blank=True)
	facebook_id = models.CharField("My Facebook account", max_length=50, null=True, blank=True)
	
	def get_activities(self):
		activities = Shareditem.objects.filter(author=self.user).select_subclasses()
		return activities
