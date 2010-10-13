# Create your models here.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib import admin
from blog.managers import PublicManager
from feincms.content.application.models import ApplicationContent

from django.db.models import CharField
from django.utils.encoding import force_unicode
from django.template.defaultfilters import slugify

from feincms.content.image.models import ImageContent
from feincms.content.richtext.models import RichTextContent
import ImageFile

import os
import datetime
import tagging
from tagging.fields import TagField

def _get_field(instance, name):
    try:
        return getattr(instance, name)
    except AttributeError:
        raise ValueError("Model %s has no field '%s'" % \
                             (instance.__class__.__name__, name))

class AutoSlugField(CharField):
    """ A SlugField that automatically populate itself using the value of another
    field.

    In addition to CharField's usual parameters you can specify:

    populate_from (mandatory): the name of the field to be used for the slug
                               creation. ValueError will be raised at the
                               object save() time if the field does not exist.

    slugify_func: the function to apply on the value of the field.
                  If unspecified django.template.defaultfilters.slugify will be
                  used.

    append_field: the name of a field that will be appended to the slug, or
                  None. ValueError will be raised at the object save() time if
                  the field does not exist.

    prepend_field: the name of a field that will be prepended to the slug, or
                   None. ValueError will be raised at the object save() time if
                   the field does not exist.

    field_separator: the separator between the slug and the {pre, ap}pended
                     fields. The default value is u'-'.

    Unless explicitly set otherwise, the field will be created with the
    'editable' and 'db_index' parameters set respectively to False and
    True. """
    
    def __init__(self, *args, **kwargs):
        # Set editable=False if not explicitly set
        if 'editable' not in kwargs:
            kwargs['editable'] = False
            
        # Set db_index=True if not explicitly set
        if 'db_index' not in kwargs:
            kwargs['db_index'] = True

        populate_from = kwargs.pop('populate_from', None)
        slugify_func = kwargs.pop('slugify_func', slugify)
        append_field = kwargs.pop('append_field', None)
        prepend_field = kwargs.pop('prepend_field', None)
        field_separator = kwargs.pop('field_separator', u'-')
            
        if populate_from is None:
            raise ValueError("missing 'populate_from' argument")
        else:
            self._populate_from = populate_from
        
        self._slugify_func = slugify_func

        self._prepend_field = prepend_field
        self._append_field = append_field
        self._field_separator = field_separator

        super(AutoSlugField, self).__init__(*args, **kwargs)
        
    def pre_save(self, model_instance, add):
        populate_from = _get_field(model_instance, self._populate_from)
        
        make_slug = self._slugify_func

        chunks = list()

        if self._prepend_field is not None:
            prepend_field = _get_field(model_instance, self._prepend_field)
            # Prepend the field's value only if it is not empty
            if prepend_field:
                chunks.append(force_unicode(prepend_field))
        
        chunks.append(make_slug(populate_from))
                
        if self._append_field is not None:
            append_field = _get_field(model_instance, self._append_field)
            # Append the field's value only if it is not empty
            if append_field:
                chunks.append(force_unicode(append_field))

        value = self._field_separator.join(chunks)
        
        setattr(model_instance, self.attname, value)

        return value

    def get_internal_type(self):
        return 'SlugField'



def get_storage_path(instance, filename):
    return os.path.join('publications/', 'photos', filename)

class Journal(models.Model):
    name = models.CharField(blank=False,max_length=50)
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = _('journal')
        verbose_name_plural = _('journals')
        ordering  = ['name']

    def __unicode__(self):
        """Human readable string for Beamline"""
        return self.name        


class Publication(models.Model):
    title = models.TextField(_('title'), max_length=200, blank=False, help_text="Enter title into a paragraph")
    slug = models.SlugField(_('slug'), max_length=100, unique_for_date='publish')
    authors = models.CharField(_('authors'), max_length=250, blank=True)
    journal = models.ForeignKey(Journal, blank=False)
    year = models.IntegerField(_('year'), blank=False)
    citation = models.CharField(_('citation'), max_length=200, blank=False, help_text="Use format 'volume(issue), first_page-last_page",default="")
    original = models.CharField(_('DOI Reference'), blank=True, max_length=200)
    pdb_entries = models.CharField(_('PDB entries'), max_length=50, help_text="Comma-separated list of PDB codes (no spaces)", blank=True, default="") 
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now, editable=False)
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    tags = TagField()
    objects = PublicManager()

    class Meta:
        verbose_name = _('publication')
        verbose_name_plural = _('publications')
        db_table  = 'publication_index'
        ordering  = ['-year', 'authors']
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

    def get_previous_publication(self):
        return self.get_previous_by_year(status__gte=2)

    def get_next_publication(self):
        return self.get_next_by_year(status__gte=2)


class PublicationAdmin(admin.ModelAdmin):
    list_display  = ('year', 'authors')
    search_fields = ('title', 'year', 'authors', 'journal')

    class Media:
        js = ['/admin_media/tinymce/jscripts/tiny_mce/tiny_mce.js', '/admin_media/tinymce_setup/tinymce_setup.js',]

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Journal)


