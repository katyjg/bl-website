from django import http
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from objlist.views import FilteredListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.humanize.templatetags import humanize
import forms
import json
import models
from datetime import datetime, timedelta
from templatetags import tasklist_tags

# Create your views here.
class LoginRequiredMixin(object):
    """
    Provides the ability to require an authenticated user for a view
    """
    @method_decorator(login_required(login_url=reverse_lazy('tasklist-login')))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class JSONResponseMixin(object):  
    def json_response(self, data, **kwargs):   
        return http.HttpResponse(json.dumps(data),  
                                 content_type='application/json', **kwargs)  
def due_date_alarm(d):
    if d:
        if d <= datetime.today().date():
            return "<span class='Critical' style='vertical-align: middle;' title='{0}'><i class='fa fa-exclamation-circle fa-3'></i></span>".format(humanize.naturalday(d))
        elif d <= (datetime.today() + timedelta(days=7)).date():
            return "<span class='High' title='{0}'><i class='fa fa-exclamation-triangle fa-3'></i></span>".format(humanize.naturalday(d))
        else:
            return humanize.naturalday(d)
    return d


class DashboardView(TemplateView):
    template_name = 'tasklist/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['projects'] = models.Project.objects.all()
        context['issues'] = models.Issue.objects.all()
        return context

class WorkPlanningView(LoginRequiredMixin, TemplateView):
    template_name = 'tasklist/work_planning.html'
    
    def get_context_data(self, **kwargs):
        context = super(WorkPlanningView, self).get_context_data(**kwargs)
        context['permanent'] = models.Issue.objects.filter(status='permanent')
        context['projects'] = models.Project.objects.exclude(is_private=True)
        return context

class ProjectDetail(FilteredListView):
    model = models.Issue
    template_name = 'tasklist/project_detail.html'
    tools_template = 'tasklist/project_tools.html'
    paginate_by = 15
    detail_url = 'issue-detail'
    list_filter = ['kind', 'priority', 'created', 'modified']
    list_display = ['id', 'describe', 'status', 'modified']
    list_styles = {'describe': 'col-xs-5', 'id': 'col-xs-1', 'due_date': 'text-center'}
    search_fields = ['title', 'description']
    ordering_proxies = {'describe': 'title'}
    order_by = ['-created', 'priority']

    def get_list_title(self):
        return u'{0} Active Issues'.format(self.project.name)
    
    def get_queryset(self):
        try:
            self.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        except models.Project.DoesNotExist:
            raise http.Http404("Project does not exist")
        self.queryset = self.project.issues.active()
        return super(ProjectDetail, self).get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['project'] = self.project
        return context

class ProjectClosed(ProjectDetail):

    def get_list_title(self):
        return u'{0} Closed Issues'.format(self.project.name)
    
    def get_queryset(self):
        try:
            self.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        except models.Project.DoesNotExist:
            raise http.Http404("Project does not exist")
        self.queryset = self.project.issues.closed()
        return super(ProjectDetail, self).get_queryset()

class ProjectMaintenance(ProjectDetail):
    tools_template = 'tasklist/maint_tools.html'
    list_display = ['id', 'describe', 'frequency', 'modified', 'due_date']
    list_transforms = {'modified': humanize.naturalday, 'due_date': due_date_alarm }

    def get_list_title(self):
        return u'{0} Maintenance Tasks'.format(self.project.name)
    
    def get_queryset(self):
        try:
            self.project = models.Project.objects.get(pk=self.kwargs.get('pk'))
        except models.Project.DoesNotExist:
            raise http.Http404("Project does not exist")
        self.queryset = self.project.issues.maintenance()
        return super(ProjectDetail, self).get_queryset()
    
class CreateIssue(LoginRequiredMixin, CreateView):
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
        initial['issue_related'] = self.issue.related.all()     
        return initial
    
    def form_valid(self, form):
        data = form.cleaned_data
        if data['author'] != self.request.user:
            raise http.HttpResponseNotAllowed("You can't comment someone else.")
        issue_data = {}
        
        for k in ['kind', 'owner', 'due_date', 'status', 'priority']:
            ext_k = 'issue_{0}'.format(k)
            if not ext_k in data: continue
            if getattr(self.issue, k) != data[ext_k] and data[ext_k]:
                issue_data[k] = data[ext_k]
        if issue_data:
            if issue_data.get('status') == models.Issue.STATES.fixed and self.issue.kind == models.Issue.TYPES.maintenance:
                issue_data['due_date'] = datetime.today() + timedelta(weeks=(self.issue.frequency * 4))
                issue_data['status'] = models.Issue.STATES.pending
            models.Issue.objects.filter(pk=self.issue.pk).update(**issue_data)
            data['issue'].related.add(*data['issue_related'])            
        return super(IssueDetail, self).form_valid(form)
        
class IssueList(FilteredListView):
    model = models.Issue
    queryset = models.Issue.objects.active()
    template_name = 'tasklist/issue_list.html'
    tools_template = 'tasklist/list_tools.html'
    paginate_by = 15
    detail_url = 'issue-detail'
    list_filter = ['kind', 'priority', 'created', 'modified']
    list_title = 'Active Issues'
    list_display = ['project', 'id', 'describe', 'status', 'modified', 'due_date']
    list_transforms = {'due_date': tasklist_tags.alarm}
    list_styles = {'describe': 'col-xs-4', 'id': 'col-xs-1', 'due_date': 'text-center'}
    search_fields = ['title', 'description']
    ordering_proxies = {'describe': 'title'}
    order_by = ['-created', 'priority']

    def get_context_data(self, **kwargs):
        context = super(IssueList, self).get_context_data(**kwargs)
        context['projects'] = models.Project.objects.all()
        context['issues'] = models.Issue.objects.all()
        return context    
    
class ClosedIssues(IssueList):
    queryset = models.Issue.objects.closed()    
    list_title = 'Closed Issues'
    
class MaintenanceIssues(IssueList):
    queryset = models.Issue.objects.maintenance()
    list_title = 'Maintenance Issues'    
    
class ManageAttachments(CreateView):
    template_name = "tasklist/attachments.html"
    model = models.Attachment
    form_class = forms.AttachmentForm
    
    def get_initial(self):
        initial = super(ManageAttachments, self).get_initial()
        try:
            self.issue = models.Issue.objects.get(pk=self.kwargs.get('pk'))
        except models.Issue.DoesNotExist:
            raise http.Http404("Issue does not exist")
        initial['issue'] = self.issue
        initial['user'] = self.request.user
        return initial

    def get_success_url(self):
        return reverse_lazy('add-issue-attachment', kwargs={'pk': self.issue.pk})        
    
    def get_context_data(self, **kwargs):
        context = super(ManageAttachments, self).get_context_data(**kwargs)
        context['object_list'] = self.issue.attachment_set.all()
        context['issue'] = self.issue
        return context
    
    def form_valid(self, form):
        data = form.cleaned_data
        if data['user'] != self.request.user:
            raise http.HttpResponseNotAllowed("You can't add a file as someone else.")
        return super(ManageAttachments, self).form_valid(form)
