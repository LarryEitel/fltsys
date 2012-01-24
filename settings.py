import os
import sys
import posixpath

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# trying to get a clean windows virtual env
PRODUCTION_SERVERS = ['xc',]
if os.environ['COMPUTERNAME'] in PRODUCTION_SERVERS:
    PRODUCTION = True
    VENV_ROOT = PROJECT_ROOT
    sys.path.append(PROJECT_ROOT)
else:
    PRODUCTION = False
    VENV_ROOT = os.path.join( 'c:\\_envs', 'flt')
    #sys.path = []
    sys.path.append(PROJECT_ROOT)
    sys.path.append(VENV_ROOT)    
    sys.path.append(os.path.join( VENV_ROOT, 'lib'))   
    sys.path.append(os.path.join( VENV_ROOT, 'lib', 'site-packages')) 
    sys.path.append('c:\\python27')  
    sys.path.append(os.path.join('c:\\python27', 'lib'))
    sys.path.append(os.path.join('c:\\python27', 'lib', 'site-packages'))
    #print sys.path
    

DEBUG = not PRODUCTION
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

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

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    #'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'compressor.finders.CompressorFinder',
    
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",

)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_7pr#bc70r5ck6$lf)ydgk*vjsfod5rl*cz8ao8&07+a-7ia3m'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "djaml.filesystem",
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "templates"),
)

# http://stackoverflow.com/questions/6990721/whats-the-best-way-to-use-coffeescript-with-django-if-youre-developing-on-wind
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
)

COFFEESCRIPT_EXECUTABLE = "coffee"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    
    # http://stackoverflow.com/questions/7698406/how-to-configure-django-compressor-and-django-staticfiles-with-amazons-s3
    #'django.contrib.staticfiles',
    'staticfiles',
    
    'django.contrib.humanize',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'django.contrib.gis',
    "django_extensions",
    "debug_toolbar",
    #'coffeescript',
    'compressor',
    "flatblocks",
    'olwidget',
    'tastypie',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'common',
    'address',
    "core",
    "current_user",
    "boundaries",
    "world",
    'gunicorn',
    'registration',
    'en',
)

#GOOGLE_API_KEY = 'ABQIAAAA7EHoBVg-afV-31BS0PskPxQA_ihIzGih6r-gZzpca5UCE7OJZBRXZIV_rBhC-2hL5RY_qPuF6gVOPA'
#Registration Settings
ACCOUNT_ACTIVATION_DAYS = 3
DEFAULT_FROM_EMAIL = "noreply@defaultroject.com"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOG_DIR = os.path.join(VENV_ROOT, 'logs')
if not os.path.exists(LOG_DIR):
    try:
        os.mkdir(LOG_DIR)
    except:
        pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file':{
	    'level': 'DEBUG',
	    'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
	},
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'formatter': 'verbose',         # define the formatter to associate
            'filename': os.path.join(LOG_DIR, 'debug.log')  # log file
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'logview.debug': {               # define another logger
            'handlers': ['debug'],  # associate a different handler
            'level': 'DEBUG',                 # specify the logging level
            'propagate': True,
        },  
    }
}

EVERNOTE_HOST = "sandbox.evernote.com" 
EVERNOTE_CONSUMER_KEY = ''
EVERNOTE_CONSUMER_SECRET = ''
EVERNOTE_USER = ''
EVERNOTE_PW = ''

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
  
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
