from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
import views, forms

urlpatterns = patterns('',
    # field urls
    url(r'^$', views.DashboardView.as_view(), name='tasklist-dashboard'),
    url(r'^p/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^p/(?P<pk>\d+)/n/$', views.CreateIssue.as_view(), name='create-issue'),
    url(r'^p/(?P<pk>\d+)/m/$', views.ProjectMaintenance.as_view(), name='project-maintenance'),
    url(r'^p/(?P<pk>\d+)/m/n/$', views.CreateIssue.as_view(form_class=forms.MaintenanceForm), name='create-maintenance'),
    url(r'^i/(?P<pk>\d+)/$', views.IssueDetail.as_view(), name='issue-detail'),
    url(r'^i/(?P<pk>\d+)/a/$', views.ManageAttachments.as_view(), name='add-issue-attachment'),
    url(r'^login/$',  login, {'template_name': 'tasklist/login.html'}, name='tasklist-login'),
    url(r'^logout/$', logout, name='tasklist-logout'),
)
