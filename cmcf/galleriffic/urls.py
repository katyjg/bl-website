from django.conf.urls.defaults import *
from photologue.models import *

urlpatterns = patterns('galleriffic.views',
    url(r'^$',
        view='all_display',
        name='post_list'
    ),
    url(r'^(?P<slug>\w{4,5})/$',
        view='gallery_display',
        name='post_list'
    ),
)



