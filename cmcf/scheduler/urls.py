from django.conf.urls.defaults import *

from scheduler import views

urlpatterns = patterns('',
    url(r'^$', views.current_week, name='scheduler.thisweek'),
    url(r'^(?P<day>\d{4}-\d{2}-\d{2})/$', views.current_week, name='scheduler.anyweek'),
)
