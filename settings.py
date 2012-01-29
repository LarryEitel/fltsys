# -*- coding: utf-8 -*-
import sys
import os.path
import posixpath
import socket
import pinax

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(PROJECT_ROOT, "parts"))

# fabric settings
FABRIC = {
    'live': {
        'HOSTS': ['host.com'],
        'WEB_USER': 'www-data',
        'ADMIN_USER': 'admin',
        'PROJECT_ROOT': '/srv/flt',
    }
}

EVERNOTE_SANDBOX = True

# trying to get a clean windows virtual env
PRODUCTION_SERVERS = ['xc',]
if socket.gethostname() in PRODUCTION_SERVERS:
    PRODUCTION = True
    sys.path.append(FABRIC['live']['PROJECT_ROOT'])
else:
    PRODUCTION = False
    
DEBUG = not PRODUCTION
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG


# tells Pinax to use the default theme
PINAX_THEME = "default"


# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'NAME': "",
        'USER': '',
        'PASSWORD': '',
        'HOST': '', 
        'PORT': '',
    }
}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/static/"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
    os.path.join(PINAX_ROOT, "themes", PINAX_THEME, "static"),
]

STATICFILES_FINDERS = [
    "staticfiles.finders.FileSystemFinder",
    "staticfiles.finders.AppDirectoriesFinder",
    "staticfiles.finders.LegacyAppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = "cache"

# Make this unique, and don't share it with anybody.
SECRET_KEY = "!ugpp=ej+j_!_dcgau^y@c(q-o!t74)kr7n=*p(jf4c4&svkxh"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "linaro_django_pagination.middleware.PaginationMiddleware",
    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "flt.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "themes", PINAX_THEME, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "staticfiles.context_processors.static",
    
    "pinax.core.context_processors.pinax_settings",
    
    "pinax.apps.account.context_processors.account",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    #'django.contrib.gis',
    "django_extensions",
    
    "pinax.templatetags",
    
    # external
    "notification", # must be first
    "staticfiles",
    "compressor",
    "debug_toolbar",
    "djboss",
    "mailer",
    "uni_form",
    "django_openid",
    "timezones",
    "emailconfirmation",
    "announcements",
    "linaro_django_pagination",
    "idios",
    "south",
    
    # Pinax
    "pinax.apps.account",
    "pinax.apps.signup_codes",
    "pinax.apps.analytics",
    
    # project
    "meta",
    "profiles",
    "oembed",

    # comments
    "django.contrib.comments",

	# ratings
	"djangoratings",

    # interactivesomerville
    "participation",
    "home",
    "en",
    'common',
    "core",
    "current_user",
    "boundaries",
    'gunicorn',

]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

EMAIL_BACKEND = "mailer.backend.DbBackend"

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
}

AUTH_PROFILE_MODULE = "profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_AUTHENTICATION = True
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = True

AUTHENTICATION_BACKENDS = [
    "pinax.apps.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "home"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

# pagination settings
# http://packages.python.org/linaro-django-pagination/usage.html#custom-pagination-templates

PAGINATION_PREVIOUS_LINK_DECORATOR = '&larr;&nbsp;'
PAGINATION_NEXT_LINK_DECORATOR = '&nbsp;&rarr;'
PAGINATION_DISPLAY_DISABLED_PREVIOUS_LINK = True
PAGINATION_DISPLAY_DISABLED_NEXT_LINK = True
PAGINATION_DEFAULT_PAGINATION = 5
PAGINATION_DEFAULT_WINDOW = 2


LOGS_ROOT = os.path.join(PROJECT_ROOT, '_logs')
if not os.path.exists(LOGS_ROOT):
    try:
        os.mkdir(LOGS_ROOT)
    except:
        pass
    
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            #'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            'format': '%(levelname)s %(asctime)s %(message)s'
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
            'filename': os.path.join(LOGS_ROOT, 'debug.log'),
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler', # set the logging class to log to a file
            'formatter': 'verbose',         # define the formatter to associate
            'filename': os.path.join(LOGS_ROOT, 'debug.log')  # log file
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

if EVERNOTE_SANDBOX:
    EVERNOTE_HOST = "sandbox.evernote.com" 
    EVERNOTE_CONSUMER_KEY = ''
    EVERNOTE_CONSUMER_SECRET = ''
    EVERNOTE_USER = ''
    EVERNOTE_PW = ''
else:
    EVERNOTE_HOST = "evernote.com"
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
