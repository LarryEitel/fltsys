import settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG
MEDIA_DEV_MODE = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

CONTACT_EMAIL = "larry@fltsys.org"

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        #'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_ROOT,'db/fltsys.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

GOOGLE_ANALYTICS_CODE = ""

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

DEFAULT_FROM_EMAIL = ""
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 587
EMAIL_USE_TLS = True

import os
import sys

KMLDIR = os.path.join(settings.PROJECT_ROOT, "private", "kml")
JSONDIR = os.path.join(settings.PROJECT_ROOT, "private", "json")

GOOGLE_API_KEY = ''

EVERNOTE_HOST = "sandbox.evernote.com" 
EVERNOTE_CONSUMER_KEY = ''
EVERNOTE_CONSUMER_SECRET = ''
EVERNOTE_USER = ''
EVERNOTE_PW = ''

EVERNOTE_HOST = "evernote.com"
EVERNOTE_CONSUMER_KEY = ''
EVERNOTE_CONSUMER_SECRET = ''
EVERNOTE_USER = ''
EVERNOTE_PW = ''