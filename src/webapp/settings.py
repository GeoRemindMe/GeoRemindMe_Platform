#coding=utf-8


import os.path, sys
from distutils.sysconfig import get_python_lib

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(__file__)
SITE_ROOT = os.path.join(PROJECT_ROOT, 'site')
MODULES_ROOT = os.path.join(PROJECT_ROOT, 'modules')
APPS_ROOT = os.path.join(PROJECT_ROOT, 'apps')
SITEPACKAGES_ROOT = get_python_lib()

sys.path.insert(0, APPS_ROOT)
sys.path.insert(0, MODULES_ROOT)
sys.path.insert(0, SITE_ROOT)

ADMINS = (
     ('Javier Cordero Martínez', 'javier@georemindme.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', #'django.db.backends.postgresql_psycopg2', #'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'georemindme',                      # Or path to database file if using sqlite3.
        'USER': 'georemindme',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    },       
     
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True
DECIMAL_SEPARATOR = '.'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT,"media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT,"static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL+'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    ("admin_tools", os.path.join(MODULES_ROOT,"admin_tools","media","admin_tools")),
    ("webapp", os.path.join(STATIC_ROOT,"webapp",)),
    ("common", os.path.join(STATIC_ROOT,"common",)),
    ("facebookApp", os.path.join(STATIC_ROOT,"facebookApp",)),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_-4aq+0fpi(7e2h7@lyj+399^14-jd_$%m#@5wgn7l4!fyf81a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'apps.api.middleware.AuthenticateAPIMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'userena.middleware.UserenaLocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'webapp.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'socialregistration.contrib.facebook.auth.FacebookAuth',
    'socialregistration.contrib.twitter.auth.TwitterAuth',
    'socialregistration.contrib.openid.auth.OpenIDAuth',
)

AUTH_PROFILE_MODULE = "profiles.UserProfile"

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.gis',
    
    'sentry',
    'raven.contrib.django',
    
    'djcelery',
    'userena',
    'userena.contrib.umessages',
    'guardian',
    'south',
    'timezones',
    'endless_pagination',
    'datatrans',
    'oauth_provider',
    'debug_toolbar',
    'efficient',
    'jsonrpc',
    'voty',
    
    'socialregistration',
    'socialregistration.contrib.facebook',
    'socialregistration.contrib.twitter',
    'socialregistration.contrib.openid',
    'socialregistration.contrib.linkedin',
    
    'profiles',
    'cities',
    'timelines',
    'places',
    'events',
    'lists',
    'mainApp',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

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
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ugettext = lambda s: s

LANGUAGES = (
    ('es', 'Español'),
    ('en', 'English'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


ANONYMOUS_USER_ID = -1
GEOREMINDME_USER_ID = -2
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
USERENA_ACTIVATION_REQUIRED = True
USERENA_SIGNIN_REDIRECT_URL = '/dashboard/'
USERENA_SIGNUP_COMPLETE = '/dashboard/'
USERENA_REDIRECT_ON_SIGNOUT = '/'
#USERENA_USE_HTTPS = True
USERENA_MUGSHOT_DEFAULT = 'mm'
USERENA_MUGSHOT_GRAVATAR = True
USERENA_MUGSHOT_SIZE = 50

ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: "/!/%s/" % o.username,
}

FACEBOOK_APP_ID = '102408026518300'
FACEBOOK_SECRET_KEY = '1993455d7ed34cbe3cf2d20126dfc014'
FACEBOOK_REQUEST_PERMISSIONS = 'email,offline_access,user_likes,user_interests,read_friendlists,user_hometown,publish_stream'

TWITTER_CONSUMER_KEY = 'SKH1kG4z6lIFNSR8zohhwQ'
TWITTER_CONSUMER_SECRET_KEY = 'vViuzQX4H5sn1NDjTTNAZDHH4H2cbNBLPnpyrRf5Q'

# Add your LinkedIn API keys here
LINKEDIN_CONSUMER_KEY = ''
LINKEDIN_CONSUMER_SECRET_KEY = ''

# Add your Github API keys here
GITHUB_CLIENT_ID = ''
GITHUB_CLIENT_SECRET = ''
GITHUB_REQUEST_PERMISSIONS = ''

# Add your Foursquare API keys here
FOURSQUARE_CLIENT_ID = ''
FOURSQUARE_CLIENT_SECRET = ''
FOURSQUARE_REQUEST_PERMISSIONS = ''

# Add your tumblr API keys here
TUMBLR_CONSUMER_KEY = ''
TUMBLR_CONSUMER_SECRET_KEY = ''

SOCIALREGISTRATION_USE_HTTPS = True
SOCIALREGISTRATION_GENERATE_USERNAME = False

import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

GOOGLE_API_PASSWORD = {
        'google_places' : 'AIzaSyBWrR-O_l5STwv1EO7U_Y3JNOnVjexf710',
        'google_maps'   : 'ABQIAAAAmy8-KiNfSlxox5XO3XZuaRSH1N1fcQdmTcucWBDBdqkgAa1-PhQNdi8-hO-oo2Jxwbusfuv87fAKHQ',
        'google_maps_secure'   : 'ABQIAAAAmy8-KiNfSlxox5XO3XZuaRRbm4cxlIAzEOiWbFakqGuIogXqIxSbUHIBjJ6fK9mqp7YoPFzOwfQQGQ',
       }


VAVAG_PASSWORD = {
        'user': 'hhkaos',
        'key': 'aa5a44800923c44a0390cd795ff595e5efc6df7b'
}

ENDLESS_PAGINATION_PER_PAGE = 10

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    #'SHOW_TOOLBAR_CALLBACK': True,
    #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    'HIDE_DJANGO_SQL': False,
    #'TAG': 'div',
    'ENABLE_STACKTRACES' : True,
    
}