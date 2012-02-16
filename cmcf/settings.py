import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

#ADMINS will receive feedback from the website and 500 errors if they arise
ADMINS = (
    ('Kathryn', 'kathryn.janzen@lightsource.ca'),
)

#MANAGERS will receive online application forms
MANAGERS = (
    ('Kathryn', 'kathryn.janzen@lightsource.ca'),
    ('Shaun', 'shaun.labiuk@lightsource.ca'),
)

#DATABASE_ENGINE = 'sqlite3'
#DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'cmcf.db')

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'website'             # Or path to database file if using sqlite3.
DATABASE_USER = 'cmcfweb'             # Not used with sqlite3.
DATABASE_PASSWORD = 'cmcfweb123'         # Not used with sqlite3.
DATABASE_HOST = '10.52.4.19'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


TIME_ZONE = 'America/Regina'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

INTERNAL_IPS = ('70.76.64.163',)
ALLOWED_NETWORKS = ('10.52.28.0/255.255.252.0', '10.52.4.0/255.255.252.0', '10.45.2.0/255.255.252.0','10.63.240.0/255.255.252.0',)


TINYMCE_JS_URL = 'http://cmcf.lightsource.ca/admin_media/tinymce/jscripts/tiny_mce/tiny_mce.js'
TINYMCE_CONTENT_CSS_URL = '/admin_media/tinymce/jscripts/tiny_mce/themes/advanced/skins/grappelli/ui.css'

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = 'http://cmcf.lightsource.ca/admin_media/'
FEINCMS_ADMIN_MEDIA = '/feincms_media/'

SECRET_KEY = '_wn95s-apfd-442cby5m^_^ak6+5(fyn3lvnvtn7!si&o)1x^w'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware'
)

ROOT_URLCONF = 'cmcf.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'feincms',
    'feincms.module.page', 
    'feincms.module.medialibrary',

    'admin_tools.dashboard',
    'admin_tools',
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.redirects',
    #'django.contrib.admindocs',

    'cmcf',
    'scheduler',
    'glossary',
    'blog',
    'tagging',
    'slider',
    'photologue',
    'contact_form',
    'application_form',
    'publications',
    'galleriffic',
    'simplewiki',

    'mptt',
    'south',
)

COVERAGE_MODULES = ['feincms',
                    'feincms._internal',
                    'feincms.admin',
                    'feincms.admin.editor',
                    'feincms.admin.filterspecs',
                    'feincms.admin.item_editor',
                    'feincms.admin.splitpane_editor',
                    'feincms.admin.tree_editor',
                    'feincms.compat',
                    'feincms.content',
                    'feincms.content.application',
                    'feincms.content.application.models',
                    'feincms.content.comments',
                    'feincms.content.comments.models',
                    'feincms.content.contactform',
                    'feincms.content.contactform.models',
                    'feincms.content.file',
                    'feincms.content.file.models',
                    'feincms.content.image',
                    'feincms.content.image.models',
                    'feincms.content.medialibrary',
                    'feincms.content.medialibrary.models',
                    'feincms.content.raw',
                    'feincms.content.raw.models',
                    'feincms.content.richtext',
                    'feincms.content.richtext.models',
                    'feincms.content.rss',
                    'feincms.content.rss.models',
                    'feincms.content.section',
                    'feincms.content.section.models',
                    'feincms.content.table',
                    'feincms.content.table.models',
                    'feincms.content.video',
                    'feincms.content.video.models',
                    'feincms.context_processors',
                    'feincms.contrib',
                    'feincms.contrib.fields',
                    'feincms.contrib.tagging',
                    'feincms.default_settings',
                    'feincms.logging',
                    'feincms.management',
                    'feincms.management.checker',
                    'feincms.management.commands',
                    'feincms.management.commands.rebuild_mptt',
                    'feincms.management.commands.rebuild_mptt_direct',
                    'feincms.management.commands.update_rsscontent',
                    'feincms.models',
                    'feincms.module',
                    'feincms.module.blog',
                    'feincms.module.blog.admin',
                    'feincms.module.blog.extensions',
                    'feincms.module.blog.extensions.tags',
                    'feincms.module.blog.extensions.translations',
                    'feincms.module.blog.models',
                    'feincms.module.extensions',
                    'feincms.module.extensions.changedate',
                    'feincms.module.extensions.seo',
                    'feincms.module.medialibrary',
                    'feincms.module.medialibrary.admin',
                    'feincms.module.medialibrary.models',
                    'feincms.module.page',
                    'feincms.module.page.admin',
                    'feincms.module.page.extensions',
                    'feincms.module.page.extensions.ct_tracker',
                    'feincms.module.page.extensions.datepublisher',
                    'feincms.module.page.extensions.navigation',
                    'feincms.module.page.extensions.symlinks',
                    'feincms.module.page.extensions.titles',
                    'feincms.module.page.extensions.translations',
                    'feincms.module.page.models',
                    'feincms.module.page.templatetags',
                    'feincms.module.page.templatetags.feincms_page_tags',
                    'feincms.shortcuts',
                    'feincms.templatetags',
                    'feincms.templatetags.applicationcontent_tags',
                    'feincms.templatetags.feincms_compat_tags',
                    'feincms.templatetags.feincms_tags',
                    'feincms.templatetags.feincms_thumbnail',
                    'feincms.templatetags.utils',
                    'feincms.tests',
                    'feincms.tests.applicationcontent_urls',
                    'feincms.tests.navigation_extensions',
                    'feincms.translations',
                    'feincms.urls',
                    'feincms.utils',
                    'feincms.utils.html',
                    'feincms.utils.html.cleanse',
                    'feincms.utils.html.tidy',
                    'feincms.utils.templatetags',
                    'feincms.views',
                    'feincms.views.applicationcontent',
                    'feincms.views.base',
                    'feincms.views.decorators',
                    'feincms.views.generic',
                    'feincms.views.generic.create_update',
                    'feincms.views.generic.date_based',
                    'feincms.views.generic.list_detail',
                    'feincms.views.generic.simple',
                    ]


try:
    # see http://nedbatchelder.com/code/coverage/
    import coverage
    TEST_RUNNER = 'cmcf.test_utils.test_runner_with_coverage'
except ImportError:
    # run without coverage support
    pass

LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    )

# Activate this to check out the split pane editor
#FEINCMS_PAGE_USE_SPLIT_PANE_EDITOR = True

FEINCMS_TREE_EDITOR_INCLUDE_ANCESTORS = True
#FEINCMS_TIDY_HTML = True

ADMIN_TOOLS_INDEX_DASHBOARD = 'cmcf.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'cmcf.dashboard.CustomAppIndexDashboard'

try:
    from settings_local import *
except ImportError:
    pass


