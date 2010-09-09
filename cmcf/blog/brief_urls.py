from django.conf.urls.defaults import *
from blog.models import *

urlpatterns = patterns('blog.views',
    url(r'^$',
        view='news_brief',
        name='blog_posts'
    ),
)
