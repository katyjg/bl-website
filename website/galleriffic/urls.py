from django.conf.urls import *
from galleriffic import views

urlpatterns = [
    url(r'^$',
        views.gallery_display,
        name='photo_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        views.gallery_display,
        name='gallery_list'
    ),
]
