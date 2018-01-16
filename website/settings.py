from django.conf.global_settings import LOGIN_REDIRECT_URL
URL_ROOT = ''
SITE_NAME_LONG = ''
SITE_DESCRIPTION = ''
SITE_KEYWORDS = ''
SITE_NAME_SHORT = ''
BEAMLINE_ACRONYM = ''

#USO_API = "http://uso-test.clsi.ca/api/v1/"
USO_API = "http://user-portal.lightsource.ca/api/v1/"

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

_version_file = os.path.join(BASE_DIR, 'VERSION')
if os.path.exists(_version_file):
    VERSION = (file(_version_file)).readline().strip()
else:
    VERSION = '- Development -'
    
SITE_ID = 1

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'local', 'website.db'),
        'ENGINE': 'django.db.backends.sqlite3',
        }
    }

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
    os.path.join(BASE_DIR, "libs", "grappelli", "static"),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'local/media')

TEMPLATES =[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static'
            ]
        },
    },
]


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

INSTALLED_APPS = (
    'filebrowser',
    'django.contrib.admin', 
    'feincms',
    'feincms.module.page',

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
    'recaptcha2',
    'crispy_forms',
    'objlist',
    'tasklist',
)

FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = False
FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/init_tinymce.html'
FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
}
FILEBROWSER_URL_TINYMCE = STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

EMAIL_HOST_USER = "clsweb@mail.blweb"
EMAIL_HOST_PASSWORD = "clsweb123"
EMAIL_PORT = 25
EMAIL_HOST = "mail-server"

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

FILEBROWSER_SUIT_TEMPLATE = False

SITE_CONFIG = [
        {'label': 'Home', 'icon': 'ti-home', 'url': '/admin/'},
        {'app': 'page', 'label': 'Web Pages', 'icon': 'ti-share', 'url': '/admin/page/page/'},
        {'app': 'blog', 'label': 'News Items', 'icon': 'ti-star','models':('post','category')},
        {'app': 'scheduler', 'label': 'Scheduler', 'icon': 'ti-time',},
        {'app': 'application_form', 'label': 'Application Forms', 'icon': 'ti-file'},
        {'app': 'photologue', 'label': 'Photo Galleries', 'icon': 'ti-image', 'models': ('gallery','photo')},
        {'label': 'Beamline Staff', 'icon': 'ti-user', 'url':'/admin/scheduler/supportperson/'},
        {'label': 'File Manager', 'url': '/admin/filebrowser/browse', 'icon': 'ti-folder'},
        {'app': 'tasklist', 'label': 'Tasklist', 'icon': 'ti-menu-alt', 'models': ('project','milestone')},
        {'app': 'auth', 'label': 'Authorization', 'icon':'ti-user'},
        {'separator': True},
        {'label': 'Beamtime', 'icon':'ti-calendar', 'url': '/beamtime/admin'},
        {'label': 'Issue Tracker', 'icon': 'ti-menu-alt', 'url': '/issues/'},
        {'label': 'Wiki', 'icon': 'ti-pencil-alt', 'url': '/wiki/', },
]

