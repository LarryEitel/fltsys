#!/usr/bin/python
import datetime
import html2text # pip install html2text
class Note:
    def __init__(self, content):
        self.content = content
        
    def parseNoteContentToMarkDown(self):    
        self.txt = html2text.html2text(self.content.decode('us-ascii','ignore'))
        return self.txt.decode('utf-8','replace')

def getpubs():
    """Get Publisher initials and names from '__Publish Name and Initials'"""
    import html2text # pip install html2text
    import re
    from note import Note
    from models import ENNote
    
    id = 90 # in table
    title = '__Publish Name and Initials'
    pubinitialsguid = '97a296aa-9698-4e29-bf74-3baa8e131ca1'
    territorypoisguid = '658ad719-3492-4882-b0f7-f52f67a7f7fa'
    #note_pubinitials = ENNote.objects.get(guid=pubinitialsguid)
    
    note_pubinitials = ENNote.objects.get(id=90)
    
    NotePubInitials = Note(note_pubinitials.content)
    txt = NotePubInitials.parseNoteContentToMarkDown()
    reobj = re.compile(r"(?P<lastname>.+?)\s*,\s*(?P<firstname>.+?)\s*-\s*_(?P<initials>[A-Z]+)")
    match = reobj.search(txt)
    if not match:
	raise Exception("Failed to match publisher initials in: %s" % txt)
    
    publishers = {}
    for match in reobj.finditer(txt):
	publishers[match.group("initials")] = "%s, %s" % (match.group("lastname"), match.group("firstname"))
    
    return publishers      