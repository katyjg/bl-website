from django.conf.urls import *

urlpatterns = patterns('blog.views',
    url(r'^categories/(?P<slug>[-\w]+)/$',
        view='category_detail',
        name='blog_category_detail'
    ),
    url(r'^page/(?P<page>\d+)/$',
        view='post_list',
        name='blog_index_paginated'
    ),
    url(r'^$',
        view='post_list',
        name='blog_index'
    ),
)

