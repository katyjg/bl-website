from django import http
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from objlist.views import FilteredListView
import models

# Create your views here.
class DashboardView(TemplateView):
    template_name = 'tasklist/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['projects'] = models.Project.objects.all()
        context['issues'] = models.Issue.objects.all()
        return context


class ProjectDetail(FilteredListView):
    model = models.Issue
    template_name = 'tasklist/project_detail.html'
    tools_template = 'tasklist/project_tools.html'
    paginate_by = 15
    detail_url = 'issue-detail'
    list_filter = ['kind','status', 'priority', 'created', 'modified']
    list_display = ['id', 'describe', 'status', 'modified']
    list_styles = {'describe': 'col-xs-7', 'id': 'col-xs-1'}
    search_fields = ['title', 'description']
    ordering_proxies = {'describe': 'title'}
    order_by = ['-created', 'priority']

    def get_queryset(self):
        try:
            self.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        except models.Project.DoesNotExist:
            raise http.Http404("Project does not exist")
        self.list_title = u'{0} Issues'.format(self.project.name)
        self.queryset = self.project.issues.active()
        return super(ProjectDetail, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context

class CreateIssue(CreateView):
    pass

class IssueDetail(DetailView):
    pass

class EditIssue(UpdateView):
    pass

class AddIssueAttachment(CreateView):
    pass