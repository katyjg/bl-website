from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page

from feincms.content.raw.models import RawContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.application.models import ApplicationContent
from feincms.content.richtext.models import RichTextContent


from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender
from feincms.content.application.models import reverse
from feincms.content.video.models import VideoContent
from django.contrib.sitemaps import Sitemap
from django.utils.safestring import mark_safe

import mptt

Page.register_extensions('feincms.module.extensions.changedate')

Page.register_templates({
    'key': 'wp-base',
    'title': 'WP Base',
    'path': 'wp-base.html',
    'regions': (
        ('main', 'Main region'),
        ),
    })

Page.register_templates({
    'key': 'wp-gallery',
    'title': 'WP Gallery',
    'path': 'wp-gallery.html',
    'regions': (
        ('main', 'Main region'),
        ),
    })

Page.register_templates({
    'key': 'wp-home',
    'title': 'WP Home',
    'path': 'wp-home.html',
    'regions': (
        ('welcome', 'Content Slider'),
    	('announce', 'Announcements'),
        ('sidebar', 'Sidebar'),
        ('col1', 'Bottom Middle', 'inherited'),
        ('col2', 'Bottom Left', 'inherited'),
        ('col3', 'Bottom Right', 'inherited'),
        ),
    })

Page.register_templates({
    'key': 'wp-guide',
    'title': 'WP Guide',
    'path': 'wp-guide.html',
    'regions': (
	('col2', 'Main Content'),
	)
    })

Page.register_templates({
    'key': 'wp-aca-guide',
    'title': 'ACA Guide',
    'path': 'wp-aca-guide.html',
    'regions': (
    ('col2', 'Main Content'),
    )
    })

Page.register_templates({
    'key': 'wp-wcsb-base',
    'title': 'PSFaM Base',
    'path': 'wp-psfam.html',
    'regions': (
    ('main', 'Main Content'),
    ('tabs', 'Navigation Tabs'),
    )
    })

Page.register_templates({
    'key': 'wp-calendar',
    'title': 'WP Calendar',
    'path': 'wp-calendar.html',
    'regions': (
        ('col1', 'Main Column'),
        ('col2', 'Sidebar Column'),
        ('col3', 'Sidebar Top'),
        ),
    })

Page.register_templates({
    'key': 'wp-schedule',
    'title': 'WP Schedule',
    'path': 'wp-schedule.html',
    'regions': (
        ('col1', 'Main Column'),
        ('col2', 'Sidebar Column'),
        ('col3', 'Sidebar Top'),
        ),
    })

Page.register_templates({
    'key': 'wp-7_5',
    'title': 'WP 2-Col. 7/5',
    'path': 'wp-7_5.html',
    'regions': (
	('col1', 'Main (Left)'),
	('col2', 'Sidebar (Right)', 'inherited'),
	)
    })

Page.register_templates({
    'key': 'wp-5_7',
    'title': 'WP 2-Col. 5/7',
    'path': 'wp-5_7.html',
    'regions': (
	('col1', 'Sidebar (Left)'),
	('col2', 'Main (Right)', 'inherited'),
	)
    })

Page.register_templates({
    'key': 'wp-8_4',
    'title': 'WP 2-Col. 8/4',
    'path': 'wp-8_4.html',
    'regions': (
	('col1', 'Main (Left)'),
	('col2', 'Sidebar (Right)', 'inherited'),
	)
    })

Page.register_templates({
    'key': 'wp-6_6',
    'title': 'WP 2-Col. 6/6',
    'path': 'wp-6_6.html',
    'regions': (
        ('col1', 'Left Column'),
        ('col2', 'Right Column'),
        ),
    })

Page.register_templates({
    'key': 'wp-9_3',
    'title': 'WP 2-Col. 9/3',
    'path': 'wp-9_3.html',
    'regions': (
        ('col1', 'Main (Left)'),
        ('col2', 'Sidebar (Right)', 'inherited'),
        ),
    })

Page.register_templates({
    'key': 'wp-10_2',
    'title': 'WP 2-Col. 10/2',
    'path': 'wp-10_2.html',
    'regions': (
        ('col1', 'Main (Left)'),
        ('col2', 'Sidebar (Right)', 'inherited'),
        ),
    })

Page.register_templates({
    'key': 'wp-sitemap',
    'title': 'WP Sitemap',
    'path': 'wp-sitemap.html',
    'regions': (
        ),
    })

Page.register_templates({
    'key': 'wp-2_8',
    'title': 'WP 2-Col. 2/8',
    'path': 'wp-2_8.html',
    'regions': (
        ('col1', 'Left Column', 'inherited'),
        ('col2', 'Main Column (Right)'),
        ),
    })

Page.register_templates({
    'key': 'wp-2_7_3',
    'title': 'WP 3-Col. 2/7/3',
    'path': 'wp-2_7_3.html',
    'regions': (
        ('col1', 'Left Column', 'inherited'),
        ('col2', 'Main Column (Center)'),
        ('col3', 'Right Column', 'inherited'),
        ),
    })

Page.register_templates({
    'key': 'wp-monitor',
    'title': 'Monitor Display',
    'path': 'wp-monitor.html',
    'regions': (
        ('topleft', 'Top Left', 'inherited'),
        ('topright', 'Top Right', 'inherited'),
        ('bottomleft', 'Bottom Left', 'inherited'),
        ('bottomright', 'Bottom Right', 'inherited'),
        ('bottommiddle', 'Bottom Middle', 'inherited'),
        ),
    })

Page.register_templates({
    'key': 'wp-monitor-dynamic',
    'title': 'Monitor Display',
    'path': 'wp-monitor-dynamic.html',
    'regions': (
        ('main', 'Main', 'inherited'),
        ('thumbnail', 'Thumbnail'),
        ),
    })

Page.create_content_type(RichTextContent, cleanse=False)
Page.create_content_type(RawContent)
#MediaFileContent.default_create_content_type(Page)
#Page.create_content_type(ImageContent, POSITION_CHOICES=(
#    ('default', 'Default position'),
#    ('block', _('block')),
#    ('left', _('left')),
#    ('right', _('right')),
#    ))
Page.create_content_type(VideoContent, POSITION_CHOICES=(
    ('default', 'Default position'),
    ))

Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('scheduler.urls',                     'Beamline Schedule'),
    ('scheduler.import_urls',              'Imported Schedule'),
    ('scheduler.contacts_urls',            'Personnel List'),
    ('scheduler.oncall_urls',              'Local Contact Legend'),
    ('galleriffic.urls',                   'Photo Galleries'),
    ('publications.urls',                  'Publications (List)'),
    ('publications.brief_urls',            'Publications (Teaser)'),
    ('blog.urls',                          'News Items (Full)'),
    ('blog.brief_urls',                    'News Items (Teaser)'),
    ('blog.slider_urls',                   'News Items (Slider)'),
    ('contact_form.urls',                  'Feedback Form'),
    ('application_form.urls',              'Application Form'),
    ('application_form.registration_urls', 'PSFaM Registration'),
    ('application_form.abstract_urls',     'Registrant Abstracts'),
    ))    

'''Entry.register_regions(
    ('main', 'Main region'),
    )
Entry.create_content_type(RawContent)
Entry.create_content_type(ImageContent, POSITION_CHOICES=(
    ('default', 'Default position'),
))'''
    
from django.db import models as django_models
    
class Category(django_models.Model):
    name = django_models.CharField(max_length=20)
    slug = django_models.SlugField()
    parent = django_models.ForeignKey('self', blank=True, null=True, related_name='children')

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name
mptt.register(Category)

# add m2m field to entry so it shows up in entry admin
#Entry.add_to_class('categories', models.ManyToManyField(Category, blank=True, null=True))
#EntryAdmin.list_filter += ('categories',)

