#!/usr/bin/python
import markdown # pip install markdown
import html2text # pip install html2text
import sys, optparse, datetime, tempfile, os
import getpass
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types

# YOU MUST FILL THESE IN! GET ACCESS AT: http://www.evernote.com/about/developer/api/
MY_CONSUMER_KEY = ''
MY_CONSUMER_SECRET = ''
MY_USER = ''
MY_PW = ''

# try to overwrite MY_* Constants
try:
    from en_local_settings import *
except ImportError:
    pass


#TODO: Add local cahce via sqlite DB.
#TODO: allow 3 different ways of viewing converted html data: 1) markdowm, 2) regular text 3) full html text 


def GetUserCredentials():
    """Prompts the user for a username and password."""
    email = None #fill these in during testing if you want
    password = None
    if email is None:
        email = raw_input("Email: ")
        
    if password is None:
        password_prompt = "Password for %s: " % email
        password = getpass.getpass(password_prompt)

    return (email, password)
        

def printUsage():
    print "Use better"
    
class CleverNote:
    listCount = 10
    noteName = ""
    notebookName = ""
    verbose = False
    xml = False
    tags = []
    text = ""
    consumerKey = MY_CONSUMER_KEY
    consumerSecret = MY_CONSUMER_SECRET
    userStoreUri = "https://evernote.com/edam/user"
    noteStoreUriBase = "http://evernote.com/edam/note/"
    authToken = None
    authResult = None
    noteStore = None
    def getAuth(self, user, password):
        userStoreHttpClient = THttpClient.THttpClient(self.userStoreUri)
        userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
        userStore = UserStore.Client(userStoreProtocol)
    
        versionOK = userStore.checkVersion("Python EDAMTest",
                                       UserStoreConstants.EDAM_VERSION_MAJOR,
                                       UserStoreConstants.EDAM_VERSION_MINOR)
        if not versionOK:
            print "Old EDAM version"
            exit(1)
        authResult = userStore.authenticate(user, password,
                            self.consumerKey, self.consumerSecret)
        user = authResult.user
        self.authToken = authResult.authenticationToken
        self.authResult = authResult
        return self.authToken
    
    def getNoteStore(self):
        noteStoreUri = self.noteStoreUriBase + self.authResult.user.shardId
        noteStoreHttpClient = THttpClient.THttpClient(noteStoreUri)
        noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
        self.noteStore = NoteStore.Client(noteStoreProtocol)

    def parseNoteToMarkDown(self, note):    
        txt = html2text.html2text(note.decode('us-ascii','ignore'))
        return txt.decode('utf-8','replace')

    def convertToHTML(self, note):
        noteHTML = markdown.markdown(note)
        return noteHTML
    
    
    def wrapNotetoHTML(self, noteBody):
        mytext = '''<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml.dtd">
<en-note>'''
        mytext += self.convertToHTML(noteBody)
        mytext += "</en-note>"
        return mytext
        
    def createNote(self):
        
        newText = getInput()
        mytext = self.wrapNotetoHTML(newText)        
        mynote = Types.Note()
        mynote.title = self.noteName
        mynote.content = mytext
        self.noteStore.createNote(self.authToken,mynote)
              
        
    def appendNote(self):    
        noteURI = self.findNoteString(self.noteName)
        oldNote = self.tomboy.GetNoteContents(noteURI)
        print oldNote
        newText = getInput()
        oldNote = self.tomboy.GetNoteContentsXml(noteURI) 
        oldNote = oldNote[:-15] + newText + "\n</note-content>"
        self.tomboy.SetNoteContentsXml(noteURI, oldNote)
    
    def editNote(self):
        note = Types.Note()
        note = self.getNote(self.noteName, False)
        oldNote = self.parseNoteToMarkDown(note.content)
     
        (fd, tfn) = tempfile.mkstemp()
        
        os.write(fd, oldNote)
        os.close(fd)
        editor = os.environ.get("editor")
        if not (editor):
            editor = os.environ.get("EDITOR")
        if not (editor):
            editor = "vi"
        os.system(editor + " " + tfn)
        file = open(tfn, 'r')
        contents = file.read()
        try:
            noteContent = self.wrapNotetoHTML(contents)
            note.content = noteContent
            self.noteStore.updateNote(self.authToken, note)
        except:
            print "Your XML was malformed. Edit again (Y/N)?"
            answer = ""
            while (answer.lower() != 'n' and answer.lower() != 'y'):
                answer = getInput(1)
            if (answer.lower() == 'y'):
                self.editNote()
      
    def findMostRecentNote(self):
        notelist = self.getAllNotes(1)
        if (len(notelist.notes) > 0):
            notelist.notes[0].content = self.noteStore.getNoteContent(self.authToken, notelist.notes[0].guid)
            return notelist.notes[0]
        return None
    
    def displayNote(self):
        if self.noteName:
            note = self.getNote(self.noteName, False)
        else:
            note = self.findMostRecentNote()
        if (note == None):
            print "No note found with " + self.noteName
        else:
            print note.title
            print "----------"
            if (self.xml):
                print note.content
            else:
                print self.parseNoteToMarkDown(note.content)
                
        
        
    def findNotes(self, count, keywords):
        nf = NoteStore.NoteFilter()
        nf.words = keywords;
        return self.noteStore.findNotes(self.authToken, nf, 0, count)
        
    def getNote(self, name, full):
        notelist = self.findNotes(10,name)
        #for note in notelist.notes:
        if (len(notelist.notes) == 0):
            return None
        notelist.notes[0].content = self.noteStore.getNoteContent(self.authToken, notelist.notes[0].guid)
        return notelist.notes[0]
        
    
    def getAllNotes(self, maxNotes = 100000):
        #return self.noteStore.findNotes(self.authToken, NoteStore.NoteFilter(), 0, maxNotes)
        filter = NoteStore.NoteFilter()
        if self.notebookName:
            notebooks = self.noteStore.listNotebooks(self.authToken)
            notebook = [nb for nb in notebooks if nb.name == self.notebookName][0]
            if notebook:
                filter.notebookGuid = notebook.guid
        
        return self.noteStore.findNotes(self.authToken, filter, 0, maxNotes)
            
    
    def listNotes(self, listCount):
        loopCount = 0;
        notelist = self.getAllNotes(listCount)
        for note in notelist.notes:
            #assert(note,Types.Note)
            dt = datetime.datetime.fromtimestamp(note.updated/1000)
            printString = dt.strftime("%Y-%m-%d %H:%M:%S")
            tags = note.tagNames
            printString += note.title
            if tags:
                printString += "  ("
                for t in tags:
                    if ("system:notebook:" in t):                        
                        printString += t[16:]
                    else:
                        printString += t
                    printString += ", "
                printString = printString[:-2] + ")"
            print printString
            loopCount += 1
            if loopCount == listCount:
                break
    def getTerrPOIs(self):
        import simplejson as json
	import re
	
        self.notebookName = "Territory POIs"
	dstfilename = 'xts.json'
			
	notes = []
        for n in self.getAllNotes().notes:
	    note = {}
            if n.active:
		content = {}
		enml = self.noteStore.getNoteContent(self.authToken, n.guid)
		content['enml'] = enml

		match = re.search(r'"(?P<googlemaplink>http://maps\.google\.com/maps\?(?P<googlemapquerystring>.*?))"', enml, re.DOTALL | re.IGNORECASE)
		if match:
		    googlemap = {}
		    googlemap['googlemaplink'] = match.group("googlemaplink")
		    googlemap['googlemapquerystring'] = match.group("googlemapquerystring")
		    queryparams = {}
		    for queryparam in googlemap['googlemapquerystring'].split('&amp;amp;'):
			(param, val) = queryparam.split('=')
			queryparams[param] = val
			
		    googlemap['queryparams'] = queryparams	
		    
		    latlong = queryparams['ll'].split(',') if 'll' in queryparams.keys() else None
		    if latlong:
			(latitude, longitude) = latlong
			
		    googlemap['latitude'] = latitude
		    googlemap['longitude'] = longitude
		    content['googlemap'] = googlemap
		
		# extract logged activity
		#Find strings like:
		#2011-07-16 said too busy, keep trying, just got back from US, sister died.
		#01/02/2000 w Morrison, read 1st par Why wickedness. Sent link to a few MP3's.
		
		# handle: 2011-09-?? placed WT re who rules world
		# exact day is unknown
		
		# TODO. Need to convert from enml to text for the following regex to work
		#logdates_reobj = re.compile(r"((?P<ymd>(?P<ymdy>(19|20)[0-9]{2})[- /.](?P<ymdm>(0[1-9]|1[012]))[- /.](?P<ymdd>(0[1-9]|[12][0-9]|3[01])))|(?P<mdy>\b(?P<mdym>(0?[1-9]|[12][0-9]|3[01]))[- /.](?P<mdyd>(0?[1-9]|1[012]))[- /.](?P<mdyy>(19|20)?[0-9]{2})\b))\s*(?P<lognote>.*?)(?:\n|$)", re.DOTALL)

		#logdates = []
		#if logdates_reobj.match(enml):
		    ## Successful match at the start of the string
		    #for match in logdates_reobj.finditer(enml):
			#logdates.append(0)
			#x=0
			## match start: match.start()
			## match end (exclusive): match.end()
			## matched text: match.group()

		
		
                note['content'] = content
                note['guid'] = n.guid
                note['updateSequenceNum'] = n.updateSequenceNum
                note['title'] = n.title
		match = re.search("_(?P<publisher_initials>[A-Z0-9]{2,})", n.title, re.DOTALL)
		if match:
		    note['publisher_initials'] = match.group("publisher_initials")

		
		
		dt = datetime.datetime.fromtimestamp(n.updated/1000)
		note['updated'] = dt.strftime("%Y-%m-%d %H:%M:%S")
		dt = datetime.datetime.fromtimestamp(n.created/1000)
		note['created'] = dt.strftime("%Y-%m-%d %H:%M:%S")
		note['tagGuids'] = n.tagGuids
		#note['tagNames'] = n.tagNames
		note['tagNames'] = self.noteStore.getNoteTagNames(self.authToken, n.guid)
		
		attributes = {}
                attributes['author'] = n.attributes.author
		attributes['latitude'] = n.attributes.latitude
		attributes['longitude'] = n.attributes.longitude
		attributes['altitude'] = n.attributes.altitude
		attributes['sourceApplication'] = n.attributes.sourceApplication
		attributes['sourceURL'] = n.attributes.sourceURL
		
		note['attributes'] = attributes
		


		
		
		
                print note['title']
		notes.append(note)
                
        fh = open(dstfilename, 'wb')
	fh.write(json.dumps(notes).encode('utf-8'))
	fh.close()        

def argsToString(args):
    if (args):
        full_string = ""
        for a in args:
            full_string += a + " "
        full_string = full_string[:-1]
        return full_string

def processDateString(dateString):
    try:
        date = datetime.datetime.strptime(dateString, "%d/%m/%y")
    except:
        #if (verbose): print "Cannot parse date " + dateString + ". Ignoring"
        return
    return date

def va_callback(option, opt_str, value, parser):
    assert value is None
    value = []
    vals = getattr(parser.values, option.dest)
    if vals:
        for v in vals:
            value.append(v)
        value.append(",")
    rargs = parser.rargs
    while rargs:
        arg = rargs[0]

        if ((arg[:2] == "--" and len(arg) > 2) or
            (arg[:1] == "-" and len(arg) > 1 and arg[1] != "-")):
            break
        else:
            value.append(arg)
            del rargs[0]
    setattr(parser.values, option.dest, value)

def getInput():
    mystring = ""
    while(True):
        line = sys.stdin.readline()
        if not line:
            break
        mystring += line
    return mystring


if __name__ == "__main__":
    parser = optparse.OptionParser("%prog <mode> [<option>,...] [\"Note Title\"]")
    parser.add_option("-a", "--append", dest="append", action="store_true", help="Append to an existing note")
    parser.add_option("-c", "--create", dest="create", action="store_true", help="Create a new note")
    parser.add_option("-d", "--display", dest="display", action="store_true", help="Print a note to terminal")
    parser.add_option("-u", "--upload", dest="upload", action="store_true", help="Upload a note")
    parser.add_option("-U", "--uploadAll", dest="uploadAll", action="store_true", help="Upload ALL notes")
    parser.add_option("-e", "--edit", dest="edit", action="store_true", help="Interactively edit a note")
    #parser.add_option("-l", "--list", dest="list", action="callback", callback=va_callback)
    parser.add_option("-l", "--list", dest="list", action="store_true", help="List recent notes")
    parser.add_option("-L", "--listall", dest="listall", action="store_true", help="List all notes")
    parser.add_option("-n", "--notebook", dest="notebook", action="store_true", help="Use specific notebook.")
    parser.add_option("-s", "--search", dest="search", action="store_true", help="Search for text in notes")


    parser.add_option("-T", "--territorypois", dest="territorypois", action="store_true")
    parser.add_option("-t", "--tag", dest="tag", action="store")
    parser.add_option("-x", "--xml", dest="xml", action="store_true")
    parser.add_option("--no-xml", dest="forcexml", action="store_false")
    parser.add_option("--force-xml", dest="forcexml", action="store_true")
    parser.add_option("--startdate", dest="startdate", action="store")
    parser.add_option("--enddate", dest="enddate", action="store")
    parser.add_option("--count", dest="count", action="store", type="int")
    (options, args) = parser.parse_args()

    modeCount = 0
    if (options.append): modeCount += 1
    if (options.create): modeCount += 1
    if (options.display): modeCount += 1
    if (options.upload): modeCount += 1
    if (options.uploadAll): modeCount += 1
    if (options.edit): modeCount += 1
    if (options.list): modeCount += 1
    if (options.territorypois): modeCount += 1
    if (options.listall): modeCount += 1
    if (options.search): modeCount += 1
    if (modeCount < 1):
        options.list = True
    if (modeCount > 1):
        print "Only one of {append, create, display, edit, list, territorypois, search} can be specified. Use '--help' for details"
        sys.exit(1)
        
    noteName = argsToString(args)       
    listCount = 10
    if (options.count):
        listCount = options.count
    if (options.listall):
        options.list = True
        listCount = -1
        
    
    t = CleverNote()
    # (user,password) = GetUserCredentials()
    (user,password) = (MY_USER, MY_PW)
    t.getAuth(user, password)
    t.getNoteStore()
    t.noteName = noteName

    t.startDate = processDateString(options.startdate)
    t.endDate = processDateString(options.enddate)       
    
    if (options.xml):        
        t.xml = True
    
    
    if (options.append):
        t.appendNote()
        
    if (options.edit):
        t.editNote()
        
    if (options.list):
        t.listNotes(listCount)
        
    if (options.display):
        t.displayNote()

    if (options.upload):
        t.uploadNote()

    if (options.uploadAll):
        t.uploadAllNotes()

    if (options.search):
        t.search()
        
    if (options.create):
        t.createNote()
        
    if options.territorypois:
	t.getTerrPOIs()
    x=1
