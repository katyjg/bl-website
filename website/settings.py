URL_ROOT = 'http://cmcf.lightsource.ca'
SITE_NAME_SHORT = 'CMCF'

USO_API = "http://uso-test.clsi.ca/api/v1/"

########## The rest of this file shouldn't need any configuration ##############

import os, sys

PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)
sys.path.extend([PROJECT_DIR, BASE_DIR])
sys.path.extend([PROJECT_DIR, BASE_DIR, os.path.join(BASE_DIR, 'libs')])

DEBUG = True # Set to True to see full error messages in browser
TEMPLATE_DEBUG = DEBUG

_version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
if os.path.exists(_version_file):
    VERSION = (file(_version_file)).readline().strip()
else:
    VERSION = '- Development -'
    
SITE_ID = 1

# Specific IP addresses you want to have access to your wiki
INTERNAL_IPS = ()
# IP networks that you want to have access to your wiki (eg. CLS network)
ALLOWED_NETWORKS = ('10.52.28.0/255.255.252.0', '10.52.4.0/255.255.252.0', '10.45.2.0/255.255.252.0','10.63.240.0/255.255.252.0',)
ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'website.urls'

TIME_ZONE = 'America/Regina'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = 'static/'
ADMIN_MEDIA_PREFIX = URL_ROOT + '/admin_media/'
STATIC_URL = ADMIN_MEDIA_PREFIX
FEINCMS_ADMIN_MEDIA = '/feincms_media/'
FILEBROWSER_SUIT_TEMPLATE = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates/'),
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
    #'django.contrib.admindocs',

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
    
    'application_form'
)

try:
    # see http://nedbatchelder.com/code/coverage/
    import coverage
    TEST_RUNNER = 'test_utils.test_runner_with_coverage'
except ImportError:
    # run without coverage support
    pass

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    )

FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = True

FEINCMS_RICHTEXT_INIT_TEMPLATE = 'admin/content/richtext/init_tinymce.html'

FEINCMS_RICHTEXT_INIT_CONTEXT = {
    'TINYMCE_JS_URL': STATIC_URL + 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
}

LOGIN_URL = '/admin/'

try:
    from settings_local import *
except ImportError:
    pass

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
        {'app': 'scheduler', 'label': 'Scheduling', 'icon': 'icon-time'},
        {'app': 'application_form', 'label': 'Application Forms', 'icon': 'icon-file'},
        {'app': 'photologue', 'label': 'Photo Galleries', 'icon': 'icon-picture', 'models': ('gallery','photo')},
        {'app': 'simplewiki', 'label': 'Wiki', 'icon': 'icon-edit'},
        {'label': 'File Manager', 'url': '/admin/filebrowser/browse', 'icon': 'icon-folder-open'},  
        '-',
        {'label': 'Settings', 'icon': 'icon-cog', 'models': ('sites.site','redirects.redirect')},
        {'app': 'auth', 'label': 'Authorization', 'icon':'icon-user'},
        '-',
        {'label': 'Beamtime', 'icon':'icon-calendar', 'url': '/beamtime/admin'},
    ),
    'LIST_PER_PAGE': 25
}
