from django.conf.urls.defaults import *

from scheduler import views
from scheduler.models import *
from scheduler.forms import *

urlpatterns = patterns('',
    # staff calendar urls
    url(r'^admin/$', views.admin_scheduler, name='admin-scheduler.thisweek'),
    url(r'^admin/(?P<day>\d{4}-\d{2}-\d{2})/$', views.admin_scheduler, name='admin-scheduler.anyweek'),
    url(r'^staff/$', views.staff_calendar, name='staff-scheduler.thisweek'),
    url(r'^staff/(?P<day>\d{4}-\d{2}-\d{2})/$', views.staff_calendar, name='staff-scheduler.anyweek'),
    
    # action urls                   
    url(r'^add-visit/$', 
        views.add_object, {'model': Visit, 'form': AdminVisitForm, 'template': 'scheduler/form_full.html'}, 
        name='bl-add-visit'),             
    url(r'^edit-visit/(?P<id>\d+)/$', 
        views.edit_visit, {'model': Visit, 'form': AdminEditForm, 'template': 'scheduler/form_full.html'}, 
        name='bl-edit-visit'),    
    url(r'^delete-visit/(?P<id>\d+)/send/$', 
        views.delete_object, {'model': Visit, 'form': BasicForm, 'template': 'scheduler/form_full.html'}, 
        name='bl-delete-visit'),    
    url(r'^add-oncall/$',
        views.add_object, {'model': OnCall, 'form': AdminOnCallForm, 'template': 'scheduler/form_full.html'},
        name='bl-add-oncall'), 
    url(r'^delete-oncall/(?P<id>\d+)/$', 
        views.delete_object, {'model': OnCall, 'form': BasicForm, 'template': 'scheduler/form_full.html'}, 
        name='bl-delete-oncall'), 
    url(r'^get-modes/$', 
        views.add_object, {'model': Stat, 'form': AdminStatusForm, 'template': 'scheduler/form_full.html'}, 
        name='bl-add-mode'), 
)
