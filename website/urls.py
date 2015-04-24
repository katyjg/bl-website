
from blog.feeds import LatestEntries
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from feincms.contrib.preview.views import PreviewHandler
from feincms.views.cbv.views import Handler

handler = Handler.as_view()
preview_handler = PreviewHandler.as_view()

admin.autodiscover()

feeds = {
    'latest': LatestEntries,
}

urlpatterns = patterns('',
    (r'^wiki/', include('simplewiki.urls')),
    (r'^beamtime/', include('scheduler.admin_urls')),
    (r'^pubs/', include('publications.urls')),

    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/page/page/jsi18n/',     RedirectView.as_view(url='/admin/jsi18n/')),

    (r'^admin/', include(admin.site.urls)),

    url(r'^preview/(?P<page_id>\d+)/', preview_handler, name='feincms:preview'),
    url(r'^feeds/(?P<url>.*)/$', LatestEntries()),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)                                              
if settings.DEBUG:       
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT, 
            }),
    )

urlpatterns += patterns('',
    url(r'', include('feincms.urls')),
)
