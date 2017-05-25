from django.conf.urls import *
from scheduler.models import *
from scheduler import views

urlpatterns = [
    url(r'^$',
        views.contact_legend,
        name='contact_posts'
    ),
    url(
        r'^\d{4}-\d{2}-\d{2}/$', 
        views.contact_legend,
        name='contact_posts'
    ),
]
