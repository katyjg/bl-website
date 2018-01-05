from django.conf.urls import url
from scheduler.views import WeeklySchedule

urlpatterns = [
    url(r'^$', WeeklySchedule.as_view(), name='uso-schedule' )
]