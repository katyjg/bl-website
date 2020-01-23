from django.conf.urls import url
from scheduler.views import WeeklySchedule

urlpatterns = [
    url(r'^$', WeeklySchedule.as_view(), name='uso-schedule'),
    url(r'^(?P<day>\d{4}-\d{2}-\d{2})/$', WeeklySchedule.as_view(), name='uso-schedule-anyweek'),
]