from colorfield.fields import ColorField
from django.db import models
from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

from beamol.beamlines.models import BeamlinePage
from beamol.news.models import PostPage


class HomePage(Page):
    call = RichTextField(blank=True)

    announcements = RichTextField(blank=True)
    footer1 = RichTextField(blank=True)
    footer2 = RichTextField(blank=True)

    column1 = RichTextField(blank=True)
    column2 = RichTextField(blank=True)

    name_short = models.CharField(max_length=40, blank=True, )
    name_long = models.CharField(max_length=100, blank=True, )
    meta_description = models.CharField(max_length=500, blank=True, )
    meta_keywords = models.CharField(max_length=255, blank=True, )
    organization = models.CharField(max_length=100, blank=True, )
    org_url = models.URLField('Organization link', blank=True, )
    org_img = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='+')

    background = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')

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
        FieldPanel('org_img'),
    ]

    meta_content_panels = [
        FieldPanel('meta_description', classname="full"),
        FieldPanel('meta_keywords', classname="full"),
        FieldPanel('background'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(footer_content_panels, heading='Footer content'),
        ObjectList(meta_content_panels, heading='Meta content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    @staticmethod
    def news():
        return PostPage.objects.live().filter(highlight=True).order_by('-date')

    @staticmethod
    def beamlines():
        return BeamlinePage.objects.live()


class OneColumnPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], use_json_field=True, blank=True)
    submenu = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel('submenu')
    ]

    template = "wagtail-1-col.html"


class TwoColumnPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], use_json_field=True, blank=True)
    sidebar = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
    sidebar_panel = [
        FieldPanel('sidebar'),
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
    ], use_json_field=True, blank=True)

    name_short = models.CharField(max_length=40, blank=True, )
    name_long = models.CharField(max_length=100, blank=True, )
    meta_description = models.CharField(max_length=500, blank=True, )
    meta_keywords = models.CharField(max_length=255, blank=True, )
    organization = models.CharField(max_length=100, blank=True, )
    org_url = models.URLField('Organization link', blank=True, )
    org_img = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='+')

    footer1 = RichTextField(blank=True)
    footer2 = RichTextField(blank=True)

    header_color = ColorField(default='#FF0000')
    footer_color = ColorField(default='#FF0000')
    background = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('name_long', classname="full"),
        FieldPanel('name_short', classname="full"),
        FieldPanel('body'),
    ]

    footer_content_panels = [
        FieldPanel('footer1', classname="full"),
        FieldPanel('footer2', classname="full"),
        FieldPanel('organization', classname="full"),
        FieldPanel('org_url', classname="full"),
        FieldPanel('org_img'),
    ]

    meta_content_panels = [
        FieldPanel('meta_description', classname="full"),
        FieldPanel('meta_keywords', classname="full"),
        FieldPanel('header_color', classname="full"),
        FieldPanel('footer_color', classname="full"),
        FieldPanel('background'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(footer_content_panels, heading='Footer content'),
        ObjectList(meta_content_panels, heading='Meta content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])

    subpage_types = ['SubsitePage', ]

    def subsite_home(self):
        return self.specific


class SubsitePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], use_json_field=True, blank=True)

    parent_page_types = ['SubsiteHomePage', 'SubsitePage']
    subpage_types = ['SubsitePage', ]

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    def subsite_home(self, inclusive=True):
        return Page.objects.ancestor_of(self, inclusive).filter(depth=3).first().specific
