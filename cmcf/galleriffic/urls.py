from django.conf.urls import *
from photologue.models import *

urlpatterns = patterns('galleriffic.views',
    url(r'^$',
        view='gallery_display',
        name='photo_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view='gallery_display',
        name='gallery_list'
    ),
)



