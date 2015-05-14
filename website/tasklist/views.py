from django import http
from django.views.generic import DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from objlist.views import FilteredListView
import models
import forms

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
    form_class = forms.IssueForm
    template_name = "tasklist/issue_form.html"

    def get_initial(self):
        initial = super(CreateIssue, self).get_initial()
        try:
            self.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        except models.Project.DoesNotExist:
            raise http.Http404("Project does not exist")
        initial['project'] = self.project
        initial['submitter'] = self.request.user
        return initial
    
    def form_valid(self, form):
        data = form.cleaned_data
        if data['submitter'] != self.request.user:
            raise http.HttpResponseNotAllowed("You can't submit an issue as someone else.")
        return super(CreateIssue, self).form_valid(form)

class IssueDetail(CreateView):
    form_class = forms.CommentForm
    template_name = "tasklist/issue_detail.html"

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        context['issue'] = self.issue
        return context
    
    def get_initial(self):
        initial = super(IssueDetail, self).get_initial()
        try:
            self.issue = models.Issue.objects.get(pk=self.kwargs.get('pk'))
        except models.Issue.DoesNotExist:
            raise http.Http404("Issue does not exist")
        initial['issue'] = self.issue
        initial['author'] = self.request.user
        initial['issue_kind'] = self.issue.kind
        initial['issue_owner'] = self.issue.owner
        initial['issue_due_date'] = self.issue.due_date
        initial['issue_status'] = self.issue.status
        initial['issue_priority'] = self.issue.priority       
        return initial

    def form_valid(self, form):
        data = form.cleaned_data
        issue_data = {}
        labels = []
        for k in ['kind', 'owner', 'due_date', 'status', 'priority']:
            ext_k = 'issue_{0}'.format(k)
            if getattr(self.issue, k) != data[ext_k] and data[ext_k]:
                issue_data[k] = data[ext_k]
        if issue_data:
            models.Issue.objects.filter(pk=self.issue.pk).update(**issue_data)
        if data['author'] != self.request.user:
            raise http.HttpResponseNotAllowed("You can't comment someone else.")
        return super(IssueDetail, self).form_valid(form)
    
    
class EditIssue(UpdateView):
    pass

class AddIssueAttachment(CreateView):
    pass