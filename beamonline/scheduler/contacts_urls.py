from django.conf.urls import *
from scheduler.models import *
from scheduler import views

urlpatterns = [
    url(r'^$',
        views.contact_list,
        name='contact_posts'
    ),
]
