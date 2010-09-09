from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'publications.views.publication_list', {"paginate_by": 20, "template_name": 'publications/publication_list.html'}, name ="publication_index"
#        view='publication_list',
#       name='publication_index'
    ),
    url(r'^(?P<year>\d{4})/$',
        view='publications.views.publication_archive_year',
        name='publication_archive_year'
    ),
)


