from django.db import models
from django.contrib.auth.models import User
from current_user import registration
from django_extensions.db.models import TimeStampedModel
from current_user.models import CurrentUserField
from core.models import MyModel
#from django.db.models import get_model

# mysql --user=root --password= --execute="use _f; drop table flt_boundaries; drop table flt_boundaries_related_id;"

class BoundaryType(MyModel):
    owner =  CurrentUserField(blank=True, related_name = "boundary_type_owner", default=1)
    modifier = CurrentUserField(blank=True, related_name = "boundary_type_modifier", default=1)
    ispolitical = models.BooleanField("Polical?")
    istheocratic = models.BooleanField("Theocratic?")
    isterritory = models.BooleanField("Territory?")
    
    name = models.CharField("Name", max_length=128)
    fcode = models.CharField("Feature Code", max_length=10)
    title = models.CharField("Title", max_length=128, blank=True)
    
    style_id = models.PositiveSmallIntegerField("Style ID", null=True, blank=True)
    
    class Meta:
        db_table = u'flt_boundary_types' 
        ordering = ['name']
        permissions = (
            ('access_boundaries','Access to Boundary Types'), 
                       )
    def __unicode__(self):
        return self.name
                
class Boundary(MyModel):
    boundary_type = models.ForeignKey(BoundaryType)
    
    owner =  CurrentUserField(blank=True, related_name = "nam_owner", default=1)
    modifier = CurrentUserField(blank=True, related_name = "nam_modifier", default=1)
    
    related = models.ManyToManyField("self", symmetrical=False, null=True, blank=True, through='boundaries.BoundariesRelated', related_name='related_boundary')

    name = models.CharField("Name", max_length=128, blank=True)
    
    number = models.PositiveIntegerField("Number", null=True, blank=True)
    geo_name_id = models.PositiveIntegerField("GEO Name ID", null=True, blank=True)
    
    previousnumber = models.CharField("Previous Number", max_length=32, blank=True)
    
    code = models.CharField("Code", max_length=32, blank=True)
    previouscode = models.CharField("Previous Code", max_length=32, blank=True)
    
    isconfirmed = models.BooleanField("Confirmed?", )
    
    postalcode = models.CharField("Zip Code", max_length=32, blank=True)
    
    # lat lon elevation,lat lon elevation
    # one space between pt values and single comma delimit pts
    pts = models.TextField("Points", blank=True)
    
    # default center - where to render the label for this boundary
    label_pt = models.CharField("Label Point", max_length=32, blank=True)
    
    # lat lon elevation
    center_pt = models.CharField("Cener Point", max_length=32, blank=True)
    
    area_kml = models.DecimalField("Area Kilometers", max_digits=11, decimal_places=7, null=True, blank=True)
    population = models.PositiveIntegerField("Population", null=True, blank=True)
    
    population_target_language = models.PositiveIntegerField("English Population", null=True, blank=True)
    notes = models.TextField("Notes", blank=True)

    @property
    def full_name(self):
        ret = u''
        if self.boundary_type:
            ret = self.boundary_type.title
        ret += u'-' if ret else u''
        if self.name:
            ret += self.name
            
        return ret
    
    @property
    def number_path(self):
        related_title = u''
        related_title = str(self.number) if self.number else u''
        return related_title
    
    class Meta:
        #app_label = u'boundaries'
        db_table = u'flt_boundaries'        
        #unique_together = ("boundary_type", "name", "number", "code"),
        verbose_name_plural = "boundaries"
        permissions = (
            ('access_boundaries','Access to Boundaries'), 
                       )
    #def get_absolute_url(self):
        #return "/boundary/%i/" % self.id

    def type(self):
        return u'boundary'
    
    def __unicode__(self):
        return self.full_name + ' | ' + self.number_path
        #return self.name
 
    def save(self, *args, **kw):
        #if self.pri_address_mapurl:
            #match = re.search(r"&ll=(-?\d+.\d+),(-?\d+.\d+)", self.pri_address_mapurl, re.IGNORECASE)
            #if match:
                #self.pri_address_lat = match.group(1)
                #self.pri_address_long = match.group(2)

            #if 'http://' not in self.pri_address_mapurl.lower():
                #self.pri_address_mapurl = 'http://' + self.pri_address_mapurl

        #if self.webpage and 'http://' not in self.webpage.lower():
                #self.webpage = 'http://' + self.webpage

        super(Boundary, self).save(*args, **kw)
        
    
    #def add_parent(self, boundary):
        #related_boundary, created = BoundariesRelated.objects.get_or_create(
            #boundary = self,
            #parent_boundary = boundary)
        #return related_boundary
    
    #def add_child(self, boundary):
        #related_boundary, created = BoundariesRelated.objects.get_or_create(
            #boundary = self,
            #child_boundary = boundary)
        #return related_boundary
    
    
    #def remove_relationship(self, boundary):
        #BoundaryRelationship.objects.filter(
            #from_boundary=self, 
            #to_boundary=boundary).delete()
        #return        
        
    #def get_relationships(self):
        #return self.relationships.filter(
            #to_boundary__from_boundary=self)
    
    #def get_related_to(self):
        #return self.related_to.filter(
            #from_boundary__to_boundary=self)
    
    #def get_related_to(self):
        #return self.get_relationships(BOUNDARY_RELATED_TO)
    
    #def get_contained_within(self):
        #return self.get_related_to(BOUNDARY_CONTAINED_WITHIN)        
        
        

class BoundariesRelated(MyModel):
    owner =  CurrentUserField(blank=True, related_name = "boundary_related_owner", default=1)
    modifier = CurrentUserField(blank=True, related_name = "boundary_related_modifier", default=1)
    
    parent = models.ForeignKey(Boundary, db_column = 'parent_id', verbose_name="The Area Of", related_name='from_boundary')
    child = models.ForeignKey(Boundary, db_column = 'child_id', verbose_name="Includes", related_name='to_boundary')
    
    #parent_id = models.ForeignKey(Boundary, db_column = 'parent_id', verbose_name="Related From", related_name='from_boundary')
    #child_id = models.ForeignKey(Boundary, db_column = 'child_id', verbose_name="Related To", related_name='to_boundary')
    
    @property
    def full_name(self):
        related_title = u''
        related_title = self.parent.__unicode__() if self.parent else u''
        related_title += u'/' if related_title else u''
        related_title += self.child.__unicode__() if self.child else u''
        return related_title
    
    @property
    def number_path(self):
        related_title = u''
        related_title = str(self.parent.number) if self.parent.number else u''
        related_title += u'-' if related_title else u''
        related_title += str(self.child.number) if self.child.number else u''
        return related_title
    
    def __unicode__(self):
        return self.full_name + ' | ' + self.number_path
        
    class Meta:
        #app_label = u'boundaries_related'
        db_table = u'flt_boundaries_related'   
        ordering = ['parent','child']       
        
        
class B(models.Model):
    pts = models.TextField("Points", blank=True)

    class Meta:
        #app_label = u'boundaries'
        db_table = u'flt_b'  
    
    #def __unicode__(self):
        #return self.poly
 
    @property
    def poly(self):
        from django.db import connection, transaction
        cursor = connection.cursor()
        
        cursor.execute("SELECT AsText(Points) FROM flt_b WHERE id = %d LIMIT 1" % self.id)
        row = cursor.fetchone()
        return row[0].replace('POLYGON((','').replace('))','').split(',')

        
    def set_poly(self):
        from django.db import connection, transaction
        cursor = connection.cursor()
    
        # Data modifying operation - commit required
        cursor.execute("UPDATE flt_b SET Points = GeomFromText( 'POLYGON((%s))' ) WHERE id = %d" % (self.pts, self.id))
        transaction.commit_unless_managed()
 
 
    def save(self, *args, **kw):
        super(B, self).save(*args, **kw)
        self.set_poly()