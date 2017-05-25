from django.conf import settings
from django.conf.urls import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from photologue.models import Gallery, Photo

# Number of random images from the gallery to display.
SAMPLE_SIZE = ":%s" % getattr(settings, 'GALLERY_SAMPLE_SIZE', 5)

# galleries
gallery_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}

urlpatterns = [
    url(r'^gallery/(?P<slug>[\-\d\w]+)/$', DetailView.as_view(), {'slug_field': 'title_slug', 'queryset': Gallery.objects.filter(is_public=True), 'extra_context':{'sample_size':SAMPLE_SIZE}}, name='pl-gallery'),
    url(r'^gallery/page/(?P<page>[0-9]+)/$', ListView.as_view(), {'queryset': Gallery.objects.filter(is_public=True), 'allow_empty': True, 'paginate_by': 5, 'extra_context':{'sample_size':SAMPLE_SIZE}}, name='pl-gallery-list'),
]

# photographs
photo_args = {'date_field': 'date_added', 'allow_empty': True, 'queryset': Photo.objects.filter(is_public=True)}

urlpatterns += [
    url(r'^photo/(?P<slug>[\-\d\w]+)/$', DetailView.as_view(), {'slug_field': 'title_slug', 'queryset': Photo.objects.filter(is_public=True)}, name='pl-photo'),
    url(r'^photo/page/(?P<page>[0-9]+)/$', ListView.as_view(), {'queryset': Photo.objects.filter(is_public=True), 'allow_empty': True, 'paginate_by': 20}, name='pl-photo-list'),
]


