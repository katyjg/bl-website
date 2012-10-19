from django.conf.urls.defaults import *
from blog.models import *

urlpatterns = patterns('slider.views',
    url(r'^$',
        view='news_slider',
        name='blog_posts'
    ),
)
