from blog.feeds import LatestEntries
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from feincms.contrib.preview.views import PreviewHandler
from feincms.views import Handler

handler = Handler.as_view()
preview_handler = PreviewHandler.as_view()

admin.autodiscover()

feeds = {
    'latest': LatestEntries,
}

urlpatterns = [

    url(r'^admin/filebrowser/', include('filebrowser.urls')),
    url(r'^admin/page/page/jsi18n/',     RedirectView.as_view(url='/admin/jsi18n/')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^feeds/(?P<url>.*)/$', LatestEntries()),

    url(r'^{}'.format(getattr(settings, 'SIMPLE_WIKI_URL', 'wiki/')), include('simplewiki.urls')),
    url(r'^beamtime/', include('scheduler.admin_urls')),
    url(r'^pubs/', include('publications.urls')),
    url(r'^issues/', include('tasklist.urls')),
]
if settings.DEBUG:       
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static('media/', document_root=settings.MEDIA_ROOT)
#    [
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#            }),
#    ]

urlpatterns += [
    url(r'', include('feincms.contrib.preview.urls')),
    url(r'', include('feincms.urls')),
]
