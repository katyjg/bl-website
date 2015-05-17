from . import fields
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
import hashlib
import os

User = get_user_model()    

def _image_filename(instance, filename):
    return os.path.join('tasklist', 'icons', filename)

class Project(TimeStampedModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    short_description = models.CharField(verbose_name=_('Description'), max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(verbose_name=_('Private'), default=False)
    icon = models.ImageField(upload_to=_image_filename, blank=True, null=True)
            
    def __unicode__(self):
        return u'{0}'.format(self.name)

class Milestone(TimeStampedModel):
    project = models.ForeignKey(Project,)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    deadline = models.DateField(verbose_name=_('Deadline'))

    def __unicode__(self):
        return u'{0}'.format(self.name)


class IssueQuerySet(QuerySet):
    def active(self):
        return self.filter(status__in=[Issue.STATES.new, Issue.STATES.started, Issue.STATES.pending]).exclude(kind=Issue.TYPES.maintenance)

    def maintenance(self):
        return self.filter(kind__in=[Issue.TYPES.maintenance])
    
    def closed(self):
        return self.filter(status__in=[Issue.STATES.fixed, Issue.STATES.wontfix])

    def overdue(self):
        return self.filter(Q(due_date__isnull=False)&Q(due_date__lt=timezone.now())).exclude(status__in=[Issue.STATES.fixed, Issue.STATES.permanent])
        
class IssueManager(models.Manager):
    use_for_related_fields = True
    
    def get_queryset(self):
        return IssueQuerySet(self.model, using=self.db)
    
    def closed(self):
        qset = self.get_queryset()
        return qset.closed()

    def active(self):
        qset = self.get_queryset()
        return qset.active()

    def maintenance(self):
        qset = self.get_queryset()
        return qset.maintenance()

    def overdue(self): 
        return self.overdue()

class Issue(TimeStampedModel):
    TYPES = Choices(
        ('task', _('Task')),
        ('bug', _('Bug')),
        ('enhancement', _('Enhancement')),
        ('maintenance', _('Maintenance')),
    )
    STATES = Choices(
        ('new', _('New')),
        ('pending', _('Pending')),
        ('started', _('In progress')),
        ('fixed', _('Complete')),
        ('wontfix', _('Cancelled')),
        ('permanent', _('Persistent')),       
    )
    PRIORITY = Choices(
        (0, 'critical', 'Critical'),                
        (1, 'high', 'High'),
        (2, 'medium', 'Medium'),
        (3, 'low', 'Low'),
    )
    project = models.ForeignKey(Project, related_name='issues')
    milestone = models.ForeignKey(Milestone, null=True, blank=True, related_name='issues')
    title = models.CharField(verbose_name=_('Title'), max_length=250)
    description = models.TextField(verbose_name=_('Description'))
    submitter = models.ForeignKey(User, verbose_name=_('Submitter'), related_name='submitted_issues')
    owner = models.ForeignKey(User, verbose_name=_('Assigned to'), null=True, blank=True, related_name='assigned_tasks')
    status = models.CharField(max_length=20, verbose_name=_('Status'), default=STATES.new, choices=STATES)
    priority = models.IntegerField(verbose_name=_('Priority'), default=PRIORITY.medium, choices=PRIORITY)
    kind = models.CharField(max_length=20, verbose_name=_('Type'), default=TYPES.task, choices=TYPES)
    due_date = models.DateField(_('Due Date'), null=True, blank=True)
    frequency = models.IntegerField(_("Frequency"), null=True, blank=True, help_text='Number of months')
    related = models.ManyToManyField('Issue', null=True, blank=True, verbose_name="Related to", related_name="see_also")
    objects = IssueManager()
    
    def get_absolute_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.project.pk})
    
    def is_closed(self):
        return self.status in [self.STATES.fixed, self.STATES.wontfix]
    
    def get_related(self):
        if getattr(self, 'see_also'):
            return self.related.all() | self.see_also.all()
        else:
            return self.related.all()
        
    def get_latest(self):
        if getattr(self, 'comments') and self.comments.comments().count():
            return self.comments.comments().latest()
        else:
            return self
        
    def describe(self):
        txt =  u"<span>{0}</span><br/><small class='text-muted'>{1}, Priority:<span class='{2}'>{2}</span></small>".format(self.title, self.get_kind_display(), self.get_priority_display())
        return mark_safe(txt)
    describe.short_description = 'Title'
    describe.allow_tags = True
        
    def __unicode__(self):
        return u'%s' % self.title

def _attachment_filename(instance, filename):
    ext = os.path.splitext(filename)[-1]
    return os.path.join('tasklist', 'issue-files', str(instance.issue.pk), instance.slug + ext)

class Attachment(TimeStampedModel):
    user = models.ForeignKey(User, related_name='+')
    issue = models.ForeignKey(Issue)
    description = models.CharField(max_length=100, verbose_name="name")
    file = fields.RestrictedFileField(upload_to=_attachment_filename, max_size=2097152, verbose_name="<i class='fa fa-paperclip'></i>&nbsp;Attach File")
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.description = os.path.splitext(self.file.name)[0]
        hashobj = hashlib.md5(u"{0}{1}{2}{3}".format(self.file.name, self.user.pk, self.issue.pk, datetime.now().isoformat()))
        self.slug = hashobj.hexdigest()
        super(Attachment, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Attachment, self).delete(*args, **kwargs)
    
    def __unicode__(self):
        return u"{0}".format(self.description)

class CommentQuerySet(QuerySet):
    def comments(self):
        return self.filter(kind__exact=Comment.TYPES.comment)

    def updates(self):
        return self.filter(kind__exact=Comment.TYPES.update)

class CommentManager(models.Manager):
    use_for_related_fields = True
    
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self.db)
    
    def comments(self):
        qset = self.get_queryset()
        return qset.comments()

class Comment(TimeStampedModel):
    TYPES = Choices(
        ('comment', _('Comment')),
        ('update', _('Update')),
    )
    issue = models.ForeignKey(Issue, related_name='comments')
    author = models.ForeignKey(User, verbose_name=_('Author'), related_name='comments')
    description = models.TextField(verbose_name=_('Comment'), blank=True)
    kind = models.CharField(max_length=20, verbose_name=_('Type'), default=TYPES.comment, choices=TYPES)
    objects = CommentManager()

    def get_absolute_url(self):
        return reverse_lazy('issue-detail', kwargs={'pk': self.issue.pk})

    class Meta:
        get_latest_by = "created"


