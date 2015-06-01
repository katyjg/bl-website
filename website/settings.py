from django.conf.global_settings import LOGIN_REDIRECT_URL
URL_ROOT = 'http://cmcf.lightsource.ca'
SITE_NAME_LONG = 'Canadian Macromolecular Crystallography Facility'
SITE_DESCRIPTION = 'The CMCF operates macromolecular crystallography beamlines at the CLS'
SITE_KEYWORDS = 'lightsource,canadian,cls,macromolecular crystallography,protein crystallography,mxdc,autoprocess'
SITE_NAME_SHORT = 'CMCF'
BEAMLINE_ACRONYM = 'CMCF'

USO_API = "http://uso-test.clsi.ca/api/v1/"

import os
import sys
from iplist import IPAddressList

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)
sys.path.extend([PROJECT_DIR, BASE_DIR, os.path.join(BASE_DIR, 'libs'), os.path.join(BASE_DIR, 'local')])

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5ni&$-wok-8w3_my-#@08s)hcwed^2xy3-m9_0tpt-le4j-926'

DEBUG = True # Set to True to see full error messages in browser
TEMPLATE_DEBUG = DEBUG

_version_file = os.path.join(BASE_DIR, 'VERSION')
if os.path.exists(_version_file):
    VERSION = (file(_version_file)).readline().strip()
else:
    VERSION = '- Development -'
    
SITE_ID = 1

ALLOWED_HOSTS = ['*']

# Specific IP addresses or networks you want to have access to your internal pages
# such as wiki/admin etc (eg. CLS network)
INTERNAL_IPS = IPAddressList(
    '127.0.0.1/32',
	'10.52.28.0/22', 
	'10.52.4.0/22', 
	'10.45.2.0/22',
	'10.63.240.0/22',
)

# sets the number of proxies being used locally for the site
USE_X_FORWARDED_HOST = True
INTERNAL_PROXIES = 1

# Specific urls which should only be accessed from one of the internal IP addresses
# or networks above
INTERNAL_URLS = ('^/wiki', '^/admin', '^/beamtime', '^/issues')

ROOT_URLCONF = 'website.urls'
WSGI_APPLICATION = 'website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'local', 'website.db'),
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/Regina'
USE_I18N = True
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, "static"),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'local/media')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'middleware.InternalAccessMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

X_FRAME_OPTIONS = 'DENY'
#CSRF_COOKIE_HTTPONLY = True

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

INSTALLED_APPS = (
    'suit', 
    'filebrowser',    
    'django.contrib.admin', 
    'feincms',
    'feincms.module.page', 
    #'feincms.module.medialibrary',                               
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.redirects',
    'django.contrib.humanize',
    'website',
    'scheduler',
    'blog',
    'photologue',
    'contact_form',
    'publications',
    'galleriffic',
    'simplewiki',
    'mptt',
    'south',
    'captcha',    
    #'application_form',
    'crispy_forms',
    'objlist',
    'tasklist',
)

FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = True
FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_tinymce.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

EMAIL_HOST_USER = "clsweb@mail.blweb"
EMAIL_HOST_PASSWORD = "clsweb123"
EMAIL_PORT = 587

# The following is only necessary if you have included 'application_form' in the list of INSTALLED_APPS.
########################################################################################################
 
# MANAGERS will receive online application forms
MANAGERS = (
    ('TestUser', 'test.user@lightsource.ca'),
)
# Sender for application_form emails
FROM_EMAIL = 'test.user@lightsource.ca' # This should be an email that exists

# CONF_MANAGERS will receive PSFaM registration forms
CONF_MANAGERS = (
    ('TestUser', 'test.user@lightsource.ca'),
) 
# Sender email for PSFaM Registrations
CONF_FROM_EMAIL = 'test.user@lightsource.ca'
 
LOGIN_URL = '/admin/'
LOGOUT_URL = '/admin/logout/'
LOGIN_REDIRECT_URL = '/admin/'
try:
    from settings_local import *
except ImportError:
    pass

FILEBROWSER_SUIT_TEMPLATE = True
SUIT_CONFIG = {
    'ADMIN_NAME': '%s Public Website' % SITE_NAME_SHORT,
    'CONFIRM_UNSAVED_CHANGES': False,
    'MENU_ICONS': {
        'sites': 'icon-leaf',
        'auth': 'icon-lock',
        'publications': 'icon-leaf'
    },
    'MENU': (
        {'app': 'page', 'label': 'Web Pages', 'icon': 'icon-share'},
        {'app': 'blog', 'label': 'News Items', 'icon': 'icon-star','models':('post','category')},
        {'app': 'scheduler', 'label': 'Scheduler', 'icon': 'icon-time',},
        {'app': 'application_form', 'label': 'Application Forms', 'icon': 'icon-file'},
        {'app': 'photologue', 'label': 'Photo Galleries', 'icon': 'icon-picture', 'models': ('gallery','photo')},
        {'label': 'Beamline Staff', 'icon': 'icon-user', 'url':'/admin/scheduler/supportperson/'},
        {'label': 'File Manager', 'url': '/admin/filebrowser/browse', 'icon': 'icon-folder-open'},  
        {'app': 'tasklist', 'label': 'Projects', 'icon': 'icon-tasks', 'models': ('project','milestone')},
        {'label': 'Settings', 'icon': 'icon-cog', 'models': ('sites.site','redirects.redirect')},
        {'app': 'auth', 'label': 'Authorization', 'icon':'icon-user'},
        '-',
        {'label': 'Beamtime', 'icon':'icon-calendar', 'url': '/beamtime/admin'},
        {'label': 'Issue Tracker', 'icon': 'icon-tasks', 'url': '/issues/'},
        {'label': 'Wiki', 'icon': 'icon-edit', 'url': '/wiki/', },
    ),
    'LIST_PER_PAGE': 25
}

