from django.conf.urls.defaults import *
from publications.models import *
from django.conf.urls.defaults import patterns

urlpatterns = patterns('publications.views',
    url(r'^$',
        view='publications_brief',
        name='publicatoin_index'
    ),
)
