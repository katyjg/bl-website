from django.conf.urls import *
from django.views.decorators.cache import cache_page

from publications import views

urlpatterns = patterns('',
    url(r'^$', cache_page(60*60)(views.publication_list), {}, name ="publication_index"),
    url(r'^category/(?P<category>[-\w]+)$', cache_page(60*60)(views.publication_list), {}, name ="publication_category"),
)


