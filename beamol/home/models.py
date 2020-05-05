from django.db import models
from django.template.loader import render_to_string

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks, hooks

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from colorfield.fields import ColorField
from beamol.news.models import PostPage
from beamol.beamlines.models import BeamlinePage


class HomePage(Page):
    call = RichTextField(blank=True)

    announcements = RichTextField(blank=True)
    footer1 = RichTextField(blank=True)
    footer2 = RichTextField(blank=True)

    column1 = RichTextField(blank=True)
    column2 = RichTextField(blank=True)

    name_short = models.CharField(max_length=40, blank=True,)
    name_long = models.CharField(max_length=100, blank=True,)
    meta_description = models.CharField(max_length=500, blank=True,)
    meta_keywords = models.CharField(max_length=255, blank=True,)
    organization = models.CharField(max_length=100, blank=True,)
    org_url = models.URLField('Organization link', blank=True,)
    org_img = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    background = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('name_long', classname="full"),
        FieldPanel('name_short', classname="full"),
        FieldPanel('call', classname="full"),
        FieldPanel('column1', classname="full"),
        FieldPanel('column2', classname="full"),
        FieldPanel('announcements', classname="full"),
    ]

    footer_content_panels = [
        FieldPanel('footer1', classname="full"),
        FieldPanel('footer2', classname="full"),
        FieldPanel('organization', classname="full"),
        FieldPanel('org_url', classname="full"),
        ImageChooserPanel('org_img'),
    ]

    meta_content_panels = [
        FieldPanel('meta_description', classname="full"),
        FieldPanel('meta_keywords', classname="full"),
        ImageChooserPanel('background'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(footer_content_panels, heading='Footer content'),
        ObjectList(meta_content_panels, heading='Meta content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


    def news(self):
        return PostPage.objects.filter(highlight=True).order_by('date')

    def beamlines(self):
        return BeamlinePage.objects.all()


class OneColumnPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    template = "wagtail-1-col.html"


class TwoColumnPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)
    sidebar = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
    sidebar_panel = [
        StreamFieldPanel('sidebar'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Main'),
        ObjectList(sidebar_panel, heading='Sidebar'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    template = "wagtail-2-col.html"


class SubsiteHomePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)

    name_short = models.CharField(max_length=40, blank=True,)
    name_long = models.CharField(max_length=100, blank=True,)
    meta_description = models.CharField(max_length=500, blank=True,)
    meta_keywords = models.CharField(max_length=255, blank=True,)
    organization = models.CharField(max_length=100, blank=True,)
    org_url = models.URLField('Organization link', blank=True,)
    org_img = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    footer1 = RichTextField(blank=True)
    footer2 = RichTextField(blank=True)

    header_color = ColorField(default='#FF0000')
    footer_color = ColorField(default='#FF0000')
    background = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('name_long', classname="full"),
        FieldPanel('name_short', classname="full"),
        StreamFieldPanel('body'),
    ]

    footer_content_panels = [
        FieldPanel('footer1', classname="full"),
        FieldPanel('footer2', classname="full"),
        FieldPanel('organization', classname="full"),
        FieldPanel('org_url', classname="full"),
        ImageChooserPanel('org_img'),
    ]

    meta_content_panels = [
        FieldPanel('meta_description', classname="full"),
        FieldPanel('meta_keywords', classname="full"),
        FieldPanel('header_color', classname="full"),
        FieldPanel('footer_color', classname="full"),
        ImageChooserPanel('background'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(footer_content_panels, heading='Footer content'),
        ObjectList(meta_content_panels, heading='Meta content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    subpage_types = ['SubsitePage',]

    def subsite_home(self):
        return self.specific


class SubsitePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)

    parent_page_types = ['SubsiteHomePage', 'SubsitePage']
    subpage_types = ['SubsitePage',]

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    def subsite_home(self, inclusive=True):
        return Page.objects.ancestor_of(self, inclusive).filter(depth=3).first().specific

