import os

from django.conf.urls import patterns, include, url
from django.contrib import admin
#from sitemap import PageSitemap 
from blog.feeds import LatestEntries
from django.conf import settings

from django.views.generic import RedirectView

from feincms.views.cbv.views import Handler
from feincms.contrib.preview.views import PreviewHandler

handler = Handler.as_view()
preview_handler = PreviewHandler.as_view()

admin.autodiscover()

sitemaps = {
    #'pages' : PageSitemap,
}

feeds = {
    'latest': LatestEntries,
}

urlpatterns = patterns('',
    # Example:
    (r'^wiki/', include('simplewiki.urls')),
    (r'^apply/', include('application_form.urls')),
    (r'^beamtime/', include('scheduler.admin_urls')),
    (r'^pubs/', include('publications.urls')),

    # This avoids breaking Django admin's localization JavaScript when using
    # the FeinCMS frontend editing:
    
    #url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    #url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/page/page/jsi18n/',     RedirectView.as_view(url='/admin/jsi18n/')),

    (r'^admin/', include(admin.site.urls)),

    url(r'^preview/(?P<page_id>\d+)/', preview_handler, name='feincms:preview'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    #url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    url(r'^feeds/(?P<url>.*)/$', LatestEntries()),

    # This entry is here strictly for application content testing
    # XXX this really needs to go into a URLconf file which is only used by the
    # application content testcases
    #url(r'^(.*)/$', 'feincms.views.applicationcontent.handler'),
    #url(r'^(.*)/$|^$', 'feincms.views.applicationcontent.handler'),

    #url(r'^$|^(.*)/$', 'feincms.views.applicationcontent.handler'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)                                              
                       
if settings.DEBUG:       
    urlpatterns += patterns('',
                            
        (r'^feincms_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/%s/static/feincms/' % settings.ABSOLUTE_PATH_TO_FILES}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media/')}),

        (r'^admin_media/css/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': '%s/static/admin/css' % settings.ABSOLUTE_PATH_TO_FILES
            }),                        
        (r'^admin_media/img/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': '%s/static/admin/img' % settings.ABSOLUTE_PATH_TO_FILES
            }),
        (r'^admin_media/js/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': '%s/static/admin/js' % settings.ABSOLUTE_PATH_TO_FILES
            }),                                              
        (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': '%s/static' % settings.ABSOLUTE_PATH_TO_FILES
            }),                               
                            
        (r'^media/(?P<path>.*)/$', 'django.views.static.serve', {
            'document_root': '%s/cmcf/media' % settings.ABSOLUTE_PATH_TO_FILES 
            }),
        (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '%s/cmcf/media/uploads' % settings.ABSOLUTE_PATH_TO_FILES}),                            
    )

urlpatterns += patterns('',
    url(r'', include('feincms.urls')),
)
