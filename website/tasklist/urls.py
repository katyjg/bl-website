from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    # field urls
    url(r'^$', views.DashboardView.as_view(), name='tasklist-dashboard'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectDetail.as_view(), name='project-detail'),
    url(r'^project/(?P<pk>\d+)/new/$', views.CreateIssue.as_view(), name='create-issue'),
    url(r'^project/(?P<pk>\d+)/(?P<ipk>\d+)/$', views.IssueDetail.as_view(), name='issue-detail'),
    url(r'^project/(?P<pk>\d+)/(?P<ipk>\d+)/edit/$', views.EditIssue.as_view(), name='edit-issue'),
    url(r'^project/(?P<pk>\d+)/(?P<ipk>\d+)/attach/$', views.AddIssueAttachment.as_view(), name='add-issue-attachment'),
)
