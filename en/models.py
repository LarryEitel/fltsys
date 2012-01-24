from django.contrib.gis.db import models
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
    
    
    active = models.BooleanField("Active?") 
    guid = models.CharField("GUID", max_length=64, db_index=True)   
    notebookGuid = models.CharField("Notebook GUID", max_length=64)   
    notebookName = models.CharField("Notebook Name", max_length=64)   
    
   
    
    ll = models.PointField("LongLat", default='POINT(-84.145393330458063 9.9789556383996896)')
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
    
    def Update(self, note, notebookName):
        import datetime
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
    
        self.save()
    
    
    
    class Meta:
        #app_label = u'flt_evernote'
        db_table = u'flt_evernote'        
        