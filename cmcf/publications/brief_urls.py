from django.conf.urls import *
from publications.models import *

urlpatterns = patterns('publications.views',
    url(r'^$',
        view='publications_brief',
        name='publication_index'
    ),
)
