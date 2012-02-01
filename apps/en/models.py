# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
#from django.db import models
from django.contrib.auth.models import User
from current_user import registration
from django_extensions.db.models import TimeStampedModel
from current_user.models import CurrentUserField
from core.models import MyModel

class ENNote(MyModel):
    title = models.CharField("Title", max_length=1024)   
    author = models.CharField("Author", max_length=64, null=True, blank=True)  
    owner =  CurrentUserField(blank=True, related_name = "flt_evernote_owner", default=1)
    modifier = CurrentUserField(blank=True, related_name = "flt_evernote_modifier", default=1)
    
    point = models.PointField("LatLng", default='POINT(0 0)')
    active = models.BooleanField("Active?", default=False) 
    geocoded = models.BooleanField("GeoCoded?", default=False) 
    guid = models.CharField("GUID", max_length=64, db_index=True)   
    notebookGuid = models.CharField("Notebook GUID", max_length=64)   
    notebookName = models.CharField("Notebook Name", max_length=64)   
    
   
    
    #ll = models.PointField("LongLat", default='POINT(-84.145393330458063 9.9789556383996896)')
    latitude = models.FloatField("Latitude", null=True, blank=True)
    longitude = models.FloatField("Longitude", null=True, blank=True)
    altitude = models.FloatField("Altitude", null=True, blank=True)
    
    content = models.TextField("Content", null=True, blank=True) 
    encreated = models.DateTimeField("EN Created")
    enupdated = models.DateTimeField("EN Updated", null=True, blank=True)
    endeleted = models.DateTimeField("EN Deleted", null=True, blank=True)
    updateSequenceNum = models.IntegerField("Style ID", null=True, blank=True)
    objects = models.GeoManager()

    
    
    def __unicode__(self):
        return self.title
    
    def ParseDetails(self):
	import re
	import html2text # pip install html2text
	
	enml = self.content
	#contenttxt = html2text.html2text(enml.decode('us-ascii','ignore')).decode('utf-8','replace')
	contenttxt = enml
	
	# look for ll=9.999107,-84.106216 like string for lat/long
	reobj = re.compile(r"[&;]ll=(?P<latitude>[\-0-9.]+),(?P<longitude>[\-0-9.]+)")
	match = reobj.search(contenttxt)
	if match:
	    self.latitude = float(match.group("latitude"))
	    self.longitude = float(match.group("longitude"))
	    
	# look for _LWE like string for author
	# set author based on initials if possible
	reobj = re.compile(r"(^|\s|>)_?(?P<initials>[A-Z]{3})\s")
	match = reobj.search(contenttxt)
	if match:
	    initials = match.group("initials")
	    from note import getpubs
	    pubs = getpubs()
	    if initials in pubs:
		self.author = pubs[initials] + (" (_%s)" % initials)
		
	if self.latitude and self.longitude:
	    from django.contrib.gis.geos import Point
	    self.point = Point(self.latitude, self.longitude)
	    
		
	
    def UpdateFromEN(self, note, cn):
        import datetime
        import re 
	
        notebookName = cn.notebookName
	
        self.enupdated = datetime.datetime.fromtimestamp(note.updated/1000).strftime("%Y-%m-%d %H:%M:%S")
        self.encreated = datetime.datetime.fromtimestamp(note.created/1000).strftime("%Y-%m-%d %H:%M:%S")
        self.guid = note.guid
        self.title = note.title
        self.content = note.content
        self.notebookGuid = note.notebookGuid
        self.notebookName = notebookName
        self.active = note.active
        self.updateSequenceNum = note.updateSequenceNum
        if note.attributes.latitude:
            self.latitude = note.attributes.latitude
            self.longitude = note.attributes.longitude
        if note.attributes.altitude:
            self.altitude = note.attributes.altitude
        if note.attributes.author:
            self.author = note.attributes.author
	    
	
	self.ParseDetails()
        
        self.save()
    
    class Meta:
        #app_label = u'flt_evernote'
        db_table = u'flt_evernote'        
        
    
    def save(self, *args, **kw):
	self.geocoded = True if (self.latitude and self.longitude) else False
        super(ENNote, self).save(*args, **kw)
        
    