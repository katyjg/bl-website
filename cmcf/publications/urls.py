from django.conf.urls.defaults import *

from publications import views

urlpatterns = patterns('',
    url(r'^$', views.publication_list, {"paginate_by": 20, "template_name": 'publications/publication_list.html'}, name ="publication_index"),
    url(r'^(?P<year>\d{4})/$', views.publication_archive_year, name='publication_archive_year'),
    url(r'^admin/$', views.admin_publication_stats, name='admin-pub-stats'),
    url(r'^admin/extra/(?P<field>[-\w]+)$', views.admin_pub_table, name='admin-pub-table'),                        
)


