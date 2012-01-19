#import wingdbstub
from django.contrib.gis.db import models
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
                

#Create a new boundary via shell
#b = Boundary(boundary_type_id = 5, poly = 'POLYGON((-84.145393330458063 9.9789556383996896, -84.143642183664099 9.9717359981087821, -84.136791205856127 9.96863308887737, -84.135255112177205 9.9712137262579503, -84.135777384028046 9.9717667199823605, -84.135808105901617 9.9722889918331923, -84.133811184119025 9.9734257011555911, -84.13510150280932 9.9770816041114117, -84.13249014355516 9.982949481964873, -84.132643752923045 9.9830109257120299, -84.134087680981239 9.9817206070217388, -84.136944815224012 9.9815055539066915, -84.137958637052108 9.9811061695501735, -84.138450187029349 9.9827344288498239, -84.14060071817984 9.9834103100685478, -84.141675983755079 9.9819356601367879, -84.145393330458063 9.9789556383996896))')
#b.save()

class Boundary(MyModel):
    poly = models.PolygonField("Boundary", blank=True)
    isconfirmed = models.BooleanField("Confirmed?", )
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
    
    
    postalcode = models.CharField("Zip Code", max_length=32, blank=True)
    
    #area_kml = models.DecimalField("Area Kilometers", max_digits=11, decimal_places=7, null=True, blank=True)
    #population = models.PositiveIntegerField("Population", null=True, blank=True)
    
    #population_target_language = models.PositiveIntegerField("English Population", null=True, blank=True)
    notes = models.TextField("Notes", blank=True)
    
    objects = models.GeoManager()

    #helper functions
    #b = Boundary.objects.all()[0]
    #pt = b.pt_from_long_lat(-84.1453933304581, 9.97895563839969)
    #b.contains(pt)
    
    def pt_from_long_lat(self, long, lat):
        from django.contrib.gis.geos import fromstr
        return fromstr("POINT(%s %s)" % (long, lat))

    def contains(self, pt):
        return self.poly.contains(pt)
    
    # http://nemo.seaports2100.org/doku.php/tutorials/sebastian/geomysql
    # input - KML Polygon (well-formatted)
    def kml2poly(self, kml_str):
        # Begin MySQL Polygon output
        output = 'POLYGON('
     
        # Import XML parser
        from xml.dom.minidom import parseString
     
        # Parse KML kml_str
        i = parseString(kml_str)
     
        # Get outer rings coordinates
        outercoords = i.getElementsByTagName("outerBoundaryIs")[0].getElementsByTagName("coordinates")[0].firstChild.nodeValue.strip()
        
        # Start outer ring output
        output += '('
     
        # For each point in coordinates, add to output
        for pt in outercoords.split(' '):
            lon,lat,elev = pt.split(',')
            output += lon + " " + lat + ","
     
        # Strip last comma from output and close outer ring
        output = output[:-1] + ")"
     
        # Get number of inner rings
        irings = len(i.getElementsByTagName("innerBoundaryIs"))
     
        # For each inner ring, add to output
        for n in range(irings):
            # Get rind coordinates
            innercoords = i.getElementsByTagName("innerBoundaryIs")[n].getElementsByTagName("coordinates")[0].firstChild.nodeValue.strip()
     
            # Start output
            output += ",("
     
            # For each point in coordinates, add to output
            for pt in outercoords.split(' '):
                lon,lat,elev = pt.split(',')
                output += lon + " " + lat + ","
     
            # Strip last comma from output and close ring
            output = output[:-1] + ")"
     
        # End Polygon output
        output += ')'
     
        # Return formatted MySQL Polygon
        return output
         
    
    
    
    #Load poly from kml string:
    #'<Polygon><outerBoundaryIs><LinearRing><coordinates>-84.1453933305,9.9789556384,0 -84.1436421837,9.97173599811,0 -84.1367912059,9.96863308888,0 -84.1352551122,9.97121372626,0 -84.135777384,9.97176671998,0 -84.1358081059,9.97228899183,0 -84.1338111841,9.97342570116,0 -84.1351015028,9.97708160411,0 -84.1324901436,9.98294948196,0 -84.1326437529,9.98301092571,0 -84.134087681,9.98172060702,0 -84.1369448152,9.98150555391,0 -84.1379586371,9.98110616955,0 -84.138450187,9.98273442885,0 -84.1406007182,9.98341031007,0 -84.1416759838,9.98193566014,0 -84.1453933305,9.9789556384,0</coordinates></LinearRing></outerBoundaryIs></Polygon>'
    def set_poly_from_kml_str(self, kml_str):
        self.poly = self.kml2poly(kml_str)
    
    # a start for creating links to where this boundary may reside/be contained within
    def geo_tag(self):
        center_pt = self.center_pt
        bscontains = Boundary.objects.exclude(boundary_type__id=5).filter(poly__contains=center_pt)
        for b in bscontains:
            print b
    
    
    @property
    def coords(self):
        return self.poly.coords if self.poly else None
    
    @property
    def boundary(self):
        return self.poly.boundary if self.poly else None    
    
    @property
    def kml(self):
        return self.poly.kml if self.poly else None    
    
    @property
    def center_pt(self):
        return self.poly.centroid if self.poly else None      

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
        # db_table = u'flt_boundaries_test'        
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
        return self.full_name + ' | ' + self.number_path + ' : ' + str(self.id)
        #return self.name
 
    #def save(self, *args, **kw):
        ##if not self.label_pt:
            ##from django.contrib.gis.geos import GEOSGeometry           
            ###self.label_pt = self.pt_from_long_lat(pt[0], pt[1])
            ##pt = self.center_pt
            ##self.label_pt = GEOSGeometry('POINT(%s %s)' % (pt[0], pt[1]))
            ###self.label_pt = 'POINT(%s %s)' % (pt[0], pt[1])
            
        ##if self.pri_address_mapurl:
            ##match = re.search(r"&ll=(-?\d+.\d+),(-?\d+.\d+)", self.pri_address_mapurl, re.IGNORECASE)
            ##if match:
                ##self.pri_address_lat = match.group(1)
                ##self.pri_address_long = match.group(2)

            ##if 'http://' not in self.pri_address_mapurl.lower():
                ##self.pri_address_mapurl = 'http://' + self.pri_address_mapurl

        ##if self.webpage and 'http://' not in self.webpage.lower():
                ##self.webpage = 'http://' + self.webpage

        #super(Boundary, self).save(*args, **kw)
        
    
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