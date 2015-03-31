from django.conf.urls import *
from django.views.decorators.cache import cache_page

from publications import views

urlpatterns = patterns('',
    url(r'^$', cache_page(60*5)(views.publications_brief), name='publication_recent'),
)
