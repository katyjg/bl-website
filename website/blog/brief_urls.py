from django.conf.urls import *
from blog.models import *
from blog import views

urlpatterns = [
    url(r'^$',
        views.news_brief,
        name='blog_posts'
    ),
]
