import wingdbstub
import sys
import hashlib
import binascii
import time
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

import settings
username = settings.EVERNOTE_USER
password = settings.EVERNOTE_PW
consumerKey = settings.EVERNOTE_CONSUMER_KEY
consumerSecret = settings.EVERNOTE_CONSUMER_SECRET

evernoteHost = "evernote.com"
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
    authResult = userStore.authenticate(username, password,
                                        consumerKey, consumerSecret)
except Errors.EDAMUserException as e:
    # See http://www.evernote.com/about/developer/api/ref/UserStore.html#Fn_UserStore_authenticate
    parameter = e.parameter
    errorCode = e.errorCode
    errorText = Errors.EDAMErrorCode._VALUES_TO_NAMES[errorCode]
    
    raise Exception("Authentication failed (parameter: " + parameter + " errorCode: " + errorText + ")")
    

user = authResult.user
authToken = authResult.authenticationToken

noteStoreUri =  noteStoreUriBase + user.shardId
noteStoreHttpClient = THttpClient.THttpClient(noteStoreUri)
noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
noteStore = NoteStore.Client(noteStoreProtocol)

guid = '9b0129d1-b083-4351-8fd9-38fb63d7a7df'
withContent = True
withResourcesData = False
withResourcesRecognition = False
withResourcesAlternateData = False


note = noteStore.getNote(authToken, guid, withContent, withResourcesData, withResourcesRecognition, withResourcesAlternateData)

noteStore.updateNote(authToken, note)

print note.title
print note.content
print "Successfully add a new note: ", note.guid
