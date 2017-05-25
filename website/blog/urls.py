from django.conf.urls import *
from blog import views

urlpatterns = [
    url(r'^categories/(?P<slug>[-\w]+)/$',
        views.category_detail,
        name='blog_category_detail'
    ),
    url(r'^page/(?P<page>\d+)/$',
        views.post_list,
        name='blog_index_paginated'
    ),
    url(r'^$',
        views.post_list,
        name='blog_index'
    ),
]

