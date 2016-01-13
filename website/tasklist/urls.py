from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
import views, forms

urlpatterns = patterns('',
    # field urls
    url(r'^$', views.DashboardView.as_view(), name='tasklist-dashboard'),
    url(r'^p/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^p/(?P<pk>\d+)/n/$', views.CreateIssue.as_view(), name='create-issue'),
    url(r'^p/(?P<pk>\d+)/m/$', views.ProjectMaintenance.as_view(), name='project-maintenance'),
    url(r'^p/(?P<pk>\d+)/c/$', views.ProjectClosed.as_view(), name='project-closed'),
    url(r'^p/(?P<pk>\d+)/m/n/$', views.CreateIssue.as_view(form_class=forms.MaintenanceForm), name='create-maintenance'),
    url(r'^i/$', views.IssueList.as_view(), name='issue-list'),
    url(r'^i/c/$', views.ClosedIssues.as_view(), name='closed-issues'),
    url(r'^i/o/$', views.OpenIssues.as_view(), name='open-issues'),
    url(r'^i/m/$', views.MaintenanceIssues.as_view(), name='maintenance-issues'),
    url(r'^i/(?P<pk>\d+)/$', views.IssueDetail.as_view(), name='issue-detail'),
    url(r'^i/(?P<pk>\d+)/a/$', views.ManageAttachments.as_view(), name='add-issue-attachment'),
    url(r'^w/$', views.WorkPlanningView.as_view(), name='work-planning'),
    url(r'^login/$',  login, {'template_name': 'tasklist/login.html'}, name='tasklist-login'),
    url(r'^logout/$', logout, name='tasklist-logout'),
)
