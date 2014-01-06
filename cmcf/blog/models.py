from django.db import models
from ckeditor.fields import RichTextField
from filer.fields.image import FilerImageField

from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site


import os
import datetime

def get_storage_path(instance, filename):
    return os.path.join('uploads/news/', 'photos', filename)

class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ('title',)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {'slug': self.slug})


class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    author = models.ForeignKey(User, blank=True, null=True, editable=False)
    #image = models.ImageField(_('image'), blank=True, upload_to=get_storage_path)
    image = FilerImageField(blank=True, null=True)
    link = models.CharField(_('link'), blank=True, max_length=300, help_text='Link to original publication')
    citation = models.CharField(_('citation'), blank=True, max_length=300)
    body = RichTextField(_('body'), )
    tease = RichTextField(_('tease'), blank=True, help_text=_('This appears on the homepage content slider if the post is highlighted.'))
    highlight = models.BooleanField(_('highlight'), default=False, help_text=_('Should this item be featured in the content slider on the home page?'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.TextField()#TagField(editable=False)
    #objects = PublicManager()


    class Meta:
        verbose_name = _('News Item')
        verbose_name_plural = _('News Items')
        db_table  = 'blog_posts'
        ordering  = ('-publish',)
        get_latest_by = 'publish'

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('blog_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })

    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)

    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)

    def image_filename(self):
        return os.path.basename(self.image.path)


class BlogRoll(models.Model):
    """Other blogs you follow."""
    name = models.CharField(max_length=100)
    #url = models.URLField(verify_exists=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'name',)
        verbose_name = _('blog roll')
        verbose_name_plural = _('blog roll')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url


