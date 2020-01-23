from django.conf.urls import re_path
from django.urls import path

from scheduler import views
from scheduler import models
from scheduler import forms

urlpatterns = [
    # staff calendar urls
    path('admin/', views.admin_scheduler, name='admin-thisweek'),
    re_path(r'^admin/(?P<day>\d{4}-\d{2}-\d{2})/$', views.admin_scheduler, name='admin-anyweek'),
    path('staff/', views.staff_calendar, name='staff-thisweek'),
    re_path(r'^staff/(?P<day>\d{4}-\d{2}-\d{2})/$', views.staff_calendar, name='staff-anyweek'),
    
    # action urls                   
    path('add-visit/', views.add_object, {'model': models.Visit, 'form': forms.AdminVisitForm, 'template': 'scheduler/form_full.html'},
        name='bl-add-visit'),
    path('get-modes/', views.add_object,
         {'model': models.Stat, 'form': forms.AdminStatusForm, 'template': 'scheduler/form_full.html'},
         name='bl-add-mode'),
    path('breakdown/', views.get_shift_breakdown, {'template': 'scheduler/shift_breakdown.html'},
         name='bl.breakdown'),
    path('add-oncall/', views.add_object, {'model': models.OnCall, 'form': forms.AdminOnCallForm, 'template': 'scheduler/form_full.html'},
        name='bl-add-oncall'),
    re_path(r'^edit-visit/(?P<pk>\d+)/$', views.edit_visit, {'model': models.Visit, 'form': forms.AdminEditForm, 'template': 'scheduler/form_full.html'},
        name='bl-edit-visit'),    
    re_path(r'^delete-visit/(?P<pk>\d+)/send/$', views.delete_object, {'model': models.Visit, 'form': forms.DeleteForm, 'template': 'scheduler/form_full.html'},
        name='bl-delete-visit'),    
    re_path(r'^delete-oncall/(?P<pk>\d+)/$', views.delete_object, {'model': models.OnCall, 'form': forms.DeleteOnCallForm, 'template': 'scheduler/form_full.html'},
        name='bl-delete-oncall'), 
    re_path(r'^breakdown/(?P<start>\d{4}-\d{2}-\d{2})/(?P<end>\d{4}-\d{2}-\d{2})/$',
        views.get_shift_breakdown, {'template': 'scheduler/shift_breakdown.html'},
        name='bl.breakdown.dates'),
]
