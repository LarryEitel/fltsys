# https://github.com/zacharyvoase/django-boss
# http://docs.python.org/dev/library/argparse.html
from djboss.commands import *
from models import ENNote
# a copy of this file should be copied to djboss app dir
import wingdbstub

@command
def entruncatepois(args):
    from django.db import connection
    
    # TRUNCATE Existing rows
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE `{0}`'.format(ENNote._meta.db_table))  
    
    
# Load all Territory POI's
@command
@argument('howmany', type=int, help="How many notes to sync. 0 for all.")    
def enloadpois(args):
    import datetime
    from clevernote import CleverNote
    
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
        
        en.Update(notefull, notebookName)
        print "Added:", en.guid, en.title
        
        notecount += 1
        if howmany and notecount == howmany:
            break
        
    


@command
def entest(args):
    import datetime
    from clevernote import CleverNote
    cn = CleverNote()
    notebookName = "Territory POIs"
    
    print cn.listNotes(notebookName, 10)