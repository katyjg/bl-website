from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel

from news.models import PostPage
from beamlines.models import BeamlinePage


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
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(footer_content_panels, heading='Footer content'),
        ObjectList(meta_content_panels, heading='Meta content'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


    def news(self):
        return PostPage.objects.order_by('date')

    def beamlines(self):
        return BeamlinePage.objects.all()
