import os

from django.conf.urls.defaults import *
from django.contrib import admin
from sitemap import PageSitemap 
from blog.feeds import LatestEntries
from django.conf import settings

admin.autodiscover()

sitemaps = {
    'pages' : PageSitemap,
}

feeds = {
    'latest': LatestEntries,
}

urlpatterns = patterns('',
    # Example:
    (r'^photologue/', include('photologue.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin_tools/', include('admin_tools.urls')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/img/clslogo.ico'}),
    (r'^wiki/', include('simplewiki.urls')),
    (r'^apply/', include('application_form.urls')),
    (r'^beamtime/', include('scheduler.admin_urls')),

    # This avoids breaking Django admin's localization JavaScript when using
    # the FeinCMS frontend editing:
    url(r'admin/page/page/jsi18n/',     'django.views.generic.simple.redirect_to', {'url': '/admin/jsi18n/'}),

    (r'^admin/', include(admin.site.urls)),

    (r'^feincms_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/%s/media/feincms/' % settings.ABSOLUTE_PATH_TO_FILES}),
#        {'document_root': os.path.join(os.path.dirname(os.path.dirname(__file__)), 'feincms/media/feincms/')}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__), 'media/')}),

    url(r'^preview/(?P<page_id>\d+)/', 'feincms.views.base.preview_handler', name='feincms:preview'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),


    # This entry is here strictly for application content testing
    # XXX this really needs to go into a URLconf file which is only used by the
    # application content testcases
    #url(r'^(.*)/$', 'feincms.views.applicationcontent.handler'),
    #url(r'^(.*)/$|^$', 'feincms.views.applicationcontent.handler'),

    url(r'^$|^(.*)/$', 'feincms.views.applicationcontent.handler'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:       
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)/$', 'django.views.static.serve', {
            'document_root': '%s/media' % settings.ABSOLUTE_PATH_TO_FILES 
            }),
        (r'^admin_media/(?P<path>.*)/$', 'django.views.static.serve', {
            'document_root': '%s/admin_media' % settings.ABSOLUTE_PATH_TO_FILES
            }),
    )


