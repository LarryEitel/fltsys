#!/usr/bin/python
import time, datetime
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

import settings

class CleverNote:
    notebookName = "Territory POIs"  
    
    def __init__(self):
        username = settings.EVERNOTE_USER
        password = settings.EVERNOTE_PW
        consumerKey = settings.EVERNOTE_CONSUMER_KEY
        consumerSecret = settings.EVERNOTE_CONSUMER_SECRET
        evernoteHost = settings.EVERNOTE_HOST
        userStoreUri = "https://" + evernoteHost + "/edam/user"
        noteStoreUriBase = "https://" + evernoteHost + "/edam/note/"
        
        userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
        userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
        userStore = UserStore.Client(userStoreProtocol)
        
        versionOK = userStore.checkVersion("Python EDAMTest",
                                           UserStoreConstants.EDAM_VERSION_MAJOR,
                                           UserStoreConstants.EDAM_VERSION_MINOR)
        
        if not versionOK:
            raise Exception("Invalid EDAM Version")
        
        # Authenticate the user
        try :
            authResult = userStore.authenticate(username, password, consumerKey, consumerSecret)
            
        except Errors.EDAMUserException as e:
            # See http://www.evernote.com/about/developer/api/ref/UserStore.html#Fn_UserStore_authenticate
            parameter = e.parameter
            errorCode = e.errorCode
            errorText = Errors.EDAMErrorCode._VALUES_TO_NAMES[errorCode]
            
            print "Authentication failed (parameter: " + parameter + " errorCode: " + errorText + ")"
            
            if errorCode == Errors.EDAMErrorCode.INVALID_AUTH:
                if parameter == "consumerKey":
                    if consumerKey == "en-edamtest":
                        print "You must replace the variables consumerKey and consumerSecret with the values you received from Evernote."
                    else:
                        print "Your consumer key was not accepted by", evernoteHost
                        print "This sample client application requires a client API key. If you requested a web service API key, you must authenticate using OAuth."
                    print "If you do not have an API Key from Evernote, you can request one from http://www.evernote.com/about/developer/api"
                elif parameter == "username":
                    print "You must authenticate using a username and password from", evernoteHost
                    if evernoteHost != "www.evernote.com":
                        print "Note that your production Evernote account will not work on", evernoteHost
                        print "You must register for a separate test account at https://" + evernoteHost + "/Registration.action"
                elif parameter == "password":
                    print "The password that you entered is incorrect"
        
            print ""
            exit(1)
        
        userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
        userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
        self.userStore = UserStore.Client(userStoreProtocol)
    
        versionOK = self.userStore.checkVersion("Python EDAMTest",
                                       UserStoreConstants.EDAM_VERSION_MAJOR,
                                       UserStoreConstants.EDAM_VERSION_MINOR)
        if not versionOK:
            print "Old EDAM version"
            exit(1)
        authResult = self.userStore.authenticate(username, password,
                            consumerKey, consumerSecret)
        self.authToken = authResult.authenticationToken
                
        noteStoreUri = noteStoreUriBase + authResult.user.shardId
        noteStoreHttpClient = THttpClient.THttpClient(noteStoreUri)
        noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
        self.noteStore = NoteStore.Client(noteStoreProtocol) 
        
   

    #def getNote(self, name, full):
        #notelist = self.findNotes(10,name)
        ##for note in notelist.notes:
        #if (len(notelist.notes) == 0):
            #return None
        #notelist.notes[0].content = self.noteStore.getNoteContent(self.authToken, notelist.notes[0].guid)
        #return notelist.notes[0]
            

    def parseNoteContentToMarkDown(self, content):    
        txt = html2text.html2text(content.decode('us-ascii','ignore'))
        return txt.decode('utf-8','replace')
    
    def getAllNotes(self, notebookName, maxNotes = 0):
        notebooks = self.noteStore.listNotebooks(self.authToken)
        notebook = [nb for nb in notebooks if nb.name == notebookName][0]
        
        filter = NoteStore.NoteFilter()
        if notebook:
            filter.notebookGuid = notebook.guid
        
        # get total notes
        findNotes = self.noteStore.findNotes(self.authToken, filter, 0, 1)
        totalNotes = findNotes.totalNotes
        notecount = maxNotes if maxNotes and not maxNotes > totalNotes else totalNotes
        
        notelist = []
        #[noteList.append(note.name) for note in self.notes.getNotes() if note.name.startswith(text)]
        #completions = noteList

        batchsize = 50
        batchcount = 0
        
        i = 0
        while True:
            if batchcount * batchsize > notecount:
                break
            
            for note in self.noteStore.findNotes(self.authToken, filter, batchcount * batchsize, batchsize).notes: 
                notelist.append(note)
                i += 1
                if i == notecount:
                    break
                
            batchcount += 1
            
        return notelist
    
    def listNotes(self, notebookName, maxNotes = 0):
        
        loopCount = 0;
        notelist = self.getAllNotes(notebookName, maxNotes)
        for note in notelist:
            #assert(note,Types.Note)
            dt = datetime.datetime.fromtimestamp(note.updated/1000)
            printString = note.guid
            printString += ' '
            printString += dt.strftime("%Y-%m-%d %H:%M:%S")
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
            if loopCount == maxNotes:
                break            