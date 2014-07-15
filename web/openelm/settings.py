import os

from celery.schedules import crontab
import djcelery


__copyright__ = "Copyright 2011-2014 Red Robot Studios Ltd."
__license__ = "MIT http://opensource.org/licenses/MIT"


djcelery.setup_loader()


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Panic Stations', 'panic@redrobotstudios.com'),
)

MANAGERS = (
    ('Andrew Gleave', 'andrew@redrobotstudios.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

COUCHDB_SERVER = 'https://redrobot.iriscouch.com'
SECURE_COUCHDB_SERVER = 'https://redrobot.iriscouch.com'

S3_BUCKET = 'photos.openelm.org.im'

COUCHDB_ENPOINTS = {
    'public': '%s/openelm' % COUCHDB_SERVER,
    'authenticated': '%s/openelm' % SECURE_COUCHDB_SERVER
}

COUCHDB_DATABASES = (
    ('openelm.record', COUCHDB_ENPOINTS['authenticated']),
)

S3_CREDENTIALS = {
    'access_key': u'',
    'secret_key': u''
}

SERVER_EMAIL = 'notifications@openelm.org.im'
DEFAULT_FROM_EMAIL = 'notifications@openelm.org.im'
EMAIL_SUBJECT_PREFIX = '[openelm.org.im] '

BROKER_HOST = 'localhost'
BROKER_PORT = 5672
BROKER_USER = ''
BROKER_PASSWORD = ''
BROKER_VHOST = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'site', 'media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Absolute path to the directory that holds static files.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# A list of locations of additional static files
STATICFILES_DIRS = ()

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'flexo.context_processors.versioned_media',
)

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'openelm.urls'

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'couchdbkit.ext.django',
    'djcelery',
    'accounts',
    'core',
    'record',
    'public',
    'management'
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'
LOGIN_REDIRECT_URL = '/management/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request':{
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

CELERYBEAT_SCHEDULE = {
    'process_couchdb_changes': {
        'task': 'record.tasks.process_couchdb_changes',
        'schedule': crontab()
    },
    'compact_couch': {
        'task': 'record.tasks.compact_couch',
        'schedule': crontab(minute=0, hour=0)
    },
}

MEDIA_VERSION = None

# Use a local_settings.py file to override settings.
if os.path.exists(os.path.join(os.path.dirname(__file__), 'local_settings.py')):
    from local_settings import *