import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Kathryn', 'kathryn.janzen@lightsource.ca'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(os.path.dirname(__file__), 'cmcf.db')

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

TINYMCE_JS_URL = '/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js'
TINYMCE_CONTENT_CSS_URL = '/media/admin/tinymce/jscripts/tiny_mce/themes/advanced/skins/grappelli/ui.css'

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = 'http://cmcf.lightsource.ca:8000/media/admin/'
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
    '/users/kathryn/Code/cmcf-website/cmcf/templates',
    '/users/kathryn/Code/cmcf-website/cmcf/templatetags',
    '/users/kathryn/Code/cmcf-website/cmcf/galleriffic/templates',
    #'/users/kathryn/Django1.2.1',
    #'/users/kathryn/Django1.2.1/django/contrib/admin/templates/admin',
    #'/users/kathryn/FeinCMSTesting/cmcf/filebrowser/templates',
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
    'inlines',
    'tagging',
    'slider',
    'photologue',
    'contact_form',
    'publications',

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

