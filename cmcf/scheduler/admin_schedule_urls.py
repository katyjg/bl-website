from django.conf.urls.defaults import *

from scheduler import views
from scheduler.models import Visit
from scheduler.forms import *

urlpatterns = patterns('',
    url(
        r'^$', 
        views.admin_scheduler, 
        name='admin-scheduler.thisweek'
    ),
    url(
        r'^(?P<day>\d{4}-\d{2}-\d{2})/$', 
        views.admin_scheduler,
        name='admin-scheduler.anyweek'
    ),
    url(
        r'^add-visit/$', 
        views.add_object, {'model': Visit, 'form': AdminVisitForm, 'template': 'scheduler/form_full.html'}, 
        name='cmcf-add-visit'),             
    url(
        r'^edit-visit/(?P<id>\d+)/$', 
        views.edit_visit, {'model': Visit, 'form': AdminEditForm, 'template': 'scheduler/form_full.html'}, 
        name='cmcf-edit-visit'),    
    url(
        r'^delete-visit/(?P<id>\d+)/$', 
        views.delete_object, {'model': Visit, 'form': BasicForm, 'template': 'scheduler/form_full.html'}, 
        name='cmcf-delete-visit'),    
    url(
        r'^add-oncall/$',
        views.add_object, {'model': OnCall, 'form': AdminOnCallForm, 'template': 'scheduler/form_full.html'},
        name='cmcf-add-oncall'), 
    url(
        r'^delete-oncall/(?P<id>\d+)/$', 
        views.delete_object, {'model': OnCall, 'form': BasicForm, 'template': 'scheduler/form_full.html'}, 
        name='cmcf-delete-oncall'),  
)
