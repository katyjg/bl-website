# Create your models here.
from django.db import models
#from ckeditor.fields import RichTextField

from django.db.models import permalink, CharField
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.defaultfilters import slugify

import re
import os
import subprocess
import datetime

from scheduler.models import Beamline

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
    return os.path.join('publications/', 'posters', filename)

class Journal(models.Model):
    name = models.CharField(blank=False,max_length=50)
    description = models.CharField(max_length=200)
    impact_factor = models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)

    class Meta:
        verbose_name = _('journal')
        verbose_name_plural = _('journals')
        ordering  = ['name']

    def __unicode__(self):
        """Human readable string for Beamline"""
        return self.name        

class Publication(models.Model):
    MONTH_CHOICES=((1,"January"),(2,"February"),(3,"March"),(4,"April"),
                   (5,"May"),(6,"June"),(7,"July"),(8,"August"),
                   (9,"September"),(10,"October"),(11,"November"),(12,"December"))
    title = models.TextField(_('title'), max_length=200, blank=False, help_text="Enter title into a paragraph")
    slug = models.SlugField(_('slug'), max_length=100, unique_for_date='publish')
    authors = models.CharField(_('authors'), help_text="Comma-separated list of authors in format: J. Doe, M.N. Smith", max_length=500, blank=True)
    beamline = models.ManyToManyField(Beamline, blank=True)
    journal = models.ForeignKey(Journal, blank=False)
    year = models.IntegerField(_('year'), help_text="Required", blank=False)
    month = models.IntegerField(_('month'), help_text="Enter if available", choices=MONTH_CHOICES, blank=True, null=True)
    day = models.IntegerField(_('day'), help_text="Enter if available", blank=True, null=True)
    citation = models.CharField(_('citation'), max_length=200, blank=False, help_text="Use format 'volume(issue), first_page-last_page",default="")
    original = models.CharField(_('DOI Reference'), blank=True, max_length=200)
    pdb_entries = models.CharField(_('PDB entries'), max_length=100, help_text="Comma-separated list of PDB codes (no spaces)", blank=True, default="") 
    publish = models.DateTimeField(_('Date of Publication'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    tags = models.TextField()#TagField()
    #objects = models.TextField()#PublicManager()

    class Meta:
        verbose_name = _('publication')
        verbose_name_plural = _('publications')
        db_table  = 'publication_index'
        ordering  = ['-year', 'authors']
        get_latest_by = 'publish'


    def __unicode__(self):
        return u'%s' % self.title

    def display_citation(self):
        return '%s.(%s).%s.<em>%s</em> %s' % (self.authors, self.year, self.title, self.journal, self.citation)

    def get_previous_publication(self):
        return self.get_previous_by_year(status__gte=2)

    def get_next_publication(self):
        return self.get_next_by_year(status__gte=2)
    
    def get_authors(self):
        return len(self.authors) <= 35 and self.authors or '%s...' % self.authors[:35]
    
    def get_title(self):
        p = re.compile(r'<.*?>')
        title = p.sub('', self.title)
        return len(title) <= 40 and title or '%s...' % title[:40]
    
    def get_beamlines(self):
        if self.beamline.all().count() > 1: return ','.join([bl.name for bl in self.beamline.all()])
        elif self.beamline.all(): return self.beamline.all()[0].name
        else: return ''
        
    def get_pdbs(self):
        pdb_list = self.pdb_entries.replace(' ', '').split(',')
        return ( pdb_list != [''] and pdb_list ) or []
    
    
class Poster(models.Model):
    file = models.FileField(_('poster_file'), upload_to=get_storage_path, help_text="Upload a .pdf file (no larger than 10Mb)")
    title = models.TextField(_('title'), max_length=200, blank=False, help_text="Enter title into a paragraph")
    author = models.CharField(_('author'), max_length=500, blank=False)
    institution = models.CharField(max_length=500, blank=True)
    conference = models.CharField(max_length=500, blank=True)
    beamline = models.ManyToManyField(Beamline, blank=True)
    presented = models.DateField(_('presented'), default=datetime.date.today)
    created = models.DateTimeField(_('created'), auto_now_add=True, editable=False)
    modified = models.DateTimeField(_('modified'), auto_now=True)    
    
    def get_filename(self):
        return os.path.basename(self.file.path).split('.')[0]
    
    def get_imagename(self):
        if not os.path.exists((self.file.path).split('.')[0]+'.png'):
            return self.get_filename() + '-0'
        return self.get_filename() 
    
def pdf_to_png(**kwargs):
    poster = kwargs['instance']
    directory = os.path.dirname(poster.file.path)
    image_name = '%s.png' % poster.get_filename()
    if not os.path.exists(os.path.join(directory, image_name)):
        params = ['convert', poster.file.path, '-resize', '300x', os.path.join(directory, image_name)]
        try:
            subprocess.check_call(params)
        except:
            return ''
    return image_name
    
#post_save.send(sender=Poster, using='default')
post_save.connect(pdf_to_png, sender=Poster)
