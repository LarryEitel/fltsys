# https://github.com/zacharyvoase/django-boss
# http://docs.python.org/dev/library/argparse.html
from djboss.commands import *
import pprint
pp = pprint.PrettyPrinter(indent=4)

# a copy of this file should be copied to djboss app dir
#import wingdbstub


@command
def enupdtpoints(args):
    """Set point field from lat/lon"""
    
    from models import ENNote
    for note in ENNote.objects.filter(latitude__isnull = False):
        note.ParseDetails()
        note.save()
        print note.id, note.title, note.point.wkt

@command
def enpoiparseall(args):
    """Parse all map coords, authors, etc for unparsed notes"""
    
    from models import ENNote
    for note in ENNote.objects.all():
        #note.ParseDetails()
        note.save()
        print note.id, note.title

@command
def enparsedetails(args):
    from models import ENNote
    note = ENNote.objects.get(id=275)
    note.ParseDetails()
    note.save()
    x=0


@command
def enprnpubs(args):
    """Print Publisher initials and names from '__Publish Name and Initials'"""
    from note import getpubs
    pubs = getpubs()
    pp.pprint(pubs)
    
    
    
@command
def entruncatepois(args):
    from django.db import connection
    from models import ENNote
    
    # TRUNCATE Existing rows
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE `{0}`'.format(ENNote._meta.db_table))  
    
    
# Load all Territory POI's
@command
@argument('howmany', type=int, help="How many notes to sync. 0 for all.")    
def enpoisload(args):
    import datetime
    from clevernote import CleverNote
    from models import ENNote
    
    howmany = 0 if args.howmany <= 0 else args.howmany
    
    cn = CleverNote()
    notebookName = "Territory POIs"
    notecount = 0
    for note in cn.getAllNotes(notebookName, howmany):
        try:
            en = ENNote.objects.get(guid=note.guid)
            print "Exists:", en.guid, en.title
            continue
        except:
            en = ENNote()
            
        withContent = True
        withResourcesData = False
        withResourcesRecognition = False
        withResourcesAlternateData = False
        notefull = cn.noteStore.getNote(cn.authToken, note.guid, withContent, withResourcesData, withResourcesRecognition, withResourcesAlternateData)        
        
        en.UpdateFromEN(notefull, notebookName)
        print "Added:", en.guid, en.title
        
        notecount += 1
        if howmany and notecount == howmany:
            break
        
    


@command
@argument('howmany', type=int, help="How many notes to list. 0 for all.")   
def enpoislist(args):
    import datetime
    from clevernote import CleverNote
    
    howmany = 0 if args.howmany <= 0 else args.howmany
    
    cn = CleverNote()
    notebookName = "Territory POIs"
    print cn.listNotes(notebookName, howmany)