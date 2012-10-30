from django.conf.urls.defaults import *

from publications import views

urlpatterns = patterns('',
    url(r'^$', views.poster_list, {"template_name": 'publications/poster_list.html'}, name="poster-index"),
)
