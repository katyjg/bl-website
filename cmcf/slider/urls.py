from django.conf.urls import *
from blog.models import *

urlpatterns = patterns('slider.views',
    url(r'^$',
        view='news_slider',
        name='blog_posts'
    ),
)
