from django.conf.urls import *
from blog.models import *

urlpatterns = patterns('blog.views',
    url(r'^$',
        view='news_brief',
        name='blog_posts'
    ),
)
