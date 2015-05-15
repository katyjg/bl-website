from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # field urls
    url(r'^$', views.DashboardView.as_view(), name='tasklist-dashboard'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^project/(?P<pk>\d+)/new/$', views.CreateIssue.as_view(), name='create-issue'),
    url(r'^issue/(?P<pk>\d+)/$', views.IssueDetail.as_view(), name='issue-detail'),
    url(r'^issue/(?P<pk>\d+)/edit/$', views.EditIssue.as_view(), name='edit-issue'),
    url(r'^issue/(?P<pk>\d+)/attach/$', views.ManageAttachments.as_view(), name='add-issue-attachment'),
)
