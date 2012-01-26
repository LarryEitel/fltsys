from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import simplejson
from django.contrib.gis.geos import fromstr

import urllib

from participation.models import Media


class Command(BaseCommand):
	args = ""
	help = "Retrieve new photos from the Interactive Somerville Flickr group."
	
	def handle(self, *args, **options):
		
		url =  "http://api.flickr.com/services/rest/?method=flickr.groups.pools.getPhotos&api_key=%s&group_id=%s&extras=geo,description&format=json&nojsoncallback=1" % (settings.FLICKR_API_KEY, settings.FLICKR_GROUP)
		
		try:
			result = simplejson.load(urllib.urlopen(url))
			if result["stat"] == "ok":
				photos = result["photos"]
				author = User.objects.get(pk=1) # default user
				for photo in photos["photo"]:
					# check for existing photo
					existing = Media.objects.filter(url__contains=photo["id"])
					if len(existing) == 0:
						# add new photo
						media = Media()
						media.geometry = fromstr("POINT(%s %s)" % (photo["longitude"], photo["latitude"]), srid=4326)
						media.desc = "**%s**  \n%s" % (photo["title"], photo["description"]["_content"])
						media.url = "http://www.flickr.com/photos/%s/%s/in/pool-%s/" % (photo["owner"], photo["id"], settings.FLICKR_GROUP)
						media.author = author
						media.save()	
			elif result["stat"] == "fail":
				raise CommandError(result["message"])
		except: 
			raise CommandError("An Error occurred.")
			pass
			
