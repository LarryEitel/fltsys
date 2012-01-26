from django.contrib.gis.db import models
from django.db.models import permalink
from django.contrib.auth.models import User

from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType

from utils.markdowner import MarkupField
from utils.fileupload import ContentTypeRestrictedFileField
from djangoratings.fields import RatingField

from model_utils.managers import InheritanceManager

import oembed

# South introspection rules for unsupported fields
try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
	add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.LineStringField'])
	add_introspection_rules([], ['^utils\.markdowner\.MarkupField'])
	add_introspection_rules([], ['^utils\.fileupload\.ContentTypeRestrictedFileField'])
except ImportError:
	pass


def get_sentinel_user():
	""" Cascading rule if user is removed. """
	return User.objects.get_or_create(username='deleted')[0]


class Station(models.Model):
	""" A Greenline station """
	
	name = models.CharField(max_length=50)
	slug = models.SlugField(max_length=50)
	desc = MarkupField("Description", blank=True, null=True, help_text="Use <a href='http://daringfireball.net/projects/markdown/syntax'>Markdown-syntax</a>")
	
	geometry = models.PointField(geography=True) # default SRS 4326
	objects = models.GeoManager()
	
	class Meta:
		ordering = ("name",)
	
	def __unicode__(self):
		return u"%s"% (self.name)
		
	@permalink
	def get_absolute_url(self):
		return ("station_area_detail", None, { "slug": self.slug, })


class Line(models.Model):
	""" The Greenline """
	
	geometry = models.LineStringField(geography=True)
	objects = models.GeoManager()

	
class Theme(models.Model):
	""" A theme to guide and categorize user contributions and conversations"""
	
	title = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100)
	desc = MarkupField("Description", blank=True, null=True, help_text="Use <a href='http://daringfireball.net/projects/markdown/syntax'>Markdown-syntax</a>")
	
	class Meta:
		ordering = ("title",)
	
	def __unicode__(self):
		return u"%s" % self.title
		
	@permalink
	def get_absolute_url(self):
		return ("theme_detail", None, { "slug": self.slug, })
		
	def get_comment_count(self):
		return Comment.objects.for_model(self).count()
		
		
class Shareditem(models.Model):
	"""
	Parent model for all shared items on the page.
	The class is using multiple managers for 
	* inheritance and selecting subclasses (default 'objects'), and
	* for spatial queries ('geo_objects').
	"""
	
	ITEMTYPES = (
		("i", "Idea"),
		("m", "Meeting Note"),
		("n", "Newspaper Article"),
		("e", "Photo or Video"), # legacy: was 'External Media'
		("d", "Data"),
	)
	
	# used in template tags, added here for maintenance reasons
	ITEMTYPES_PLURAL = {
		"i": "Ideas",
		"m": "Meeting Notes",
		"n": "Newspaper Articles",
		"e": "Photos & Videos",
		"d": "Data",
	}
	
	desc = MarkupField("Description", help_text="Please see the <a href='#'>Text formatting cheat sheet</a> for help.")
	itemtype = models.CharField(max_length=1, choices=ITEMTYPES, )
	
	station = models.ForeignKey("Station", verbose_name="Related Station", null=True, blank=True)
	theme = models.ForeignKey("Theme", verbose_name="Related Theme", null=True, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
	
	ip = models.IPAddressField(default="127.0.0.1")
	created = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now_add=True, auto_now=True)
	
	rating = RatingField(range=5, can_change_vote=True)
	
	objects = InheritanceManager()
	
	geometry = models.PointField(geography=True, null=True, blank=True) # default SRS 4326
	geo_objects = models.GeoManager()
	
	class Meta:
		ordering = ("-created", "author")
		get_latest_by = "created"
	
	def __unicode__(self):
		return u"%i" % self.id
	
	# child model per itemtype
	CHILDMODELS = {
		"i": "idea",
		"m": "meetingnote",
		"n": "newsarticle",
		"e": "media",
		"d": "data",
	}
	
	@permalink
	def get_absolute_url(self):
		return ("%s_detail" % (Shareditem.CHILDMODELS[self.itemtype]), None, { "id": self.id, })
		
	def get_comment_count(self):
		# workaround for problem with for_model method and inheritance
		contenttype = ContentType.objects.get_for_model(self)
		return Comment.objects.filter(content_type=contenttype.id, object_pk=self.id).count()
		
	def get_child_contenttype(self):
		return ContentType.objects.get(app_label="participation", model=Shareditem.CHILDMODELS[self.itemtype])
	
	
class Idea(Shareditem):
	""" A user submitted idea relating to a station area, theme. """
	
	def save(self, *args, **kwargs):
		self.itemtype = "i"
		super(Idea, self).save(*args, **kwargs)
		
	@permalink
	def get_absolute_url(self):
		return ("idea_detail", None, { "id": self.id, })
			
		
class Meetingnote(Shareditem):
	""" A Meeting Notes/Minutes document provided via file upload or as linked resource. """
	
	meeting_date = models.DateField(help_text="Please use the 'Month/Day/Year' format", blank=True, null=True,)
	note_file = ContentTypeRestrictedFileField(
		help_text="Please upload only .pdf or .doc; max. 2.5MB.", 
		upload_to="meetingnotes", 
		content_types=["application/pdf", "application/msword", "text/plain", "application/vnd.oasis.opendocument.text", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"], 
		max_upload_size=2621440,
		blank=True, null=True, 
	)
	note_url = models.URLField("URL to external notes", null=True, blank=True)
	
	def save(self, *args, **kwargs):
		self.itemtype = "m"
		super(Meetingnote, self).save(*args, **kwargs)
		
	@permalink
	def get_absolute_url(self):
		return ("meetingnote_detail", None, { "id": self.id, })
		
		
class Newsarticle(Shareditem):
	""" A Newspaper article as linked resource. """

	url = models.URLField("URL to article", null=True, blank=True)

	def save(self, *args, **kwargs):
		self.itemtype = "n"
		super(Newsarticle, self).save(*args, **kwargs)

	@permalink
	def get_absolute_url(self):
		return ("newsarticle_detail", None, { "id": self.id, })
		
		
class Media(Shareditem):
	""" An external media item (photo, video, etc.) linked with oEmbed. """

	url = models.URLField("URL to photo or video", help_text="Please use a URL to <b>single</b> photo or video page on <a href='http://flickr.com'>Flickr</a>, <a href='http://youtube.com'>YouTube</a> or <a href='http://vimeo.com'>Vimeo</a>.", null=True, blank=True)

	class Meta:
		verbose_name_plural = "Media"

	def save(self, *args, **kwargs):
		self.itemtype = "e"
		super(Media, self).save(*args, **kwargs)

	@permalink
	def get_absolute_url(self):
		return ("media_detail", None, { "id": self.id, })
		
	
	def get_oembed(self):
		oembed.autodiscover()
		try:
			resource = oembed.site.embed(self.url)
			# Flickr doesn't provide thumbnail url through oembed
			if resource.provider_name == u"Flickr":
				resource.thumbnail_url = "%s_t.jpg" % (resource.url[:-4])
				return resource
			else:
				return resource
		except:
			pass

		
class Data(Shareditem):
	""" A data entry provided via file upload or as linked resource. """

	data_file = ContentTypeRestrictedFileField(
		help_text="Please upload only .xls, .csv., .zip, .kml/kmz, .json; max. 10MB.", 
		upload_to="data", 
		content_types=["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.oasis.opendocument.spreadsheet", "text/csv", "application/json", "application/zip", "application/vnd.google-earth.kml+xml", "application/vnd.google-earth.kmz"], 
		max_upload_size=10485760,
		blank=True, null=True, 
	)
	data_url = models.URLField("URL to other data", null=True, blank=True)

	def save(self, *args, **kwargs):
		self.itemtype = "d"
		super(Data, self).save(*args, **kwargs)
		
	@permalink
	def get_absolute_url(self):
		return ("data_detail", None, { "id": self.id, })
