from django.db import models
from django.shortcuts import render

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks, hooks

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from colorfield.fields import ColorField
from beamol.news.models import PostPage

import requests


@hooks.register('register_rich_text_features')
def register_features(features):
    features.default_features += ['code','blockquote','superscript','subscript','strikethrough']


class ImageCarouselBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.TextBlock(required=False)

    class Meta:
        icon = 'image'


class BeamlinePage(Page):
    STATUS_COLORS = (
        ('success', 'Normal Operations'),
        ('warning', 'Maintenance'),
        ('dark', 'Shutdown'),
        ('info', 'Upgrade in Progress'),
    )
    name = models.CharField(max_length=255, blank=True,)
    acronym = models.CharField(max_length=255, blank=True, )
    description = RichTextField(blank=True)
    snippet = RichTextField(blank=True, help_text="To be displayed on other parts of the site.")
    sidebar = RichTextField(blank=True)
    schematic = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='+')
    status = models.CharField(max_length=255, blank=True)
    status_color = ColorField(default='#00FF00')
    gallery = StreamField([
        ('image', blocks.ListBlock(ImageCarouselBlock(), template='beamlines/blocks/gallery.html', icon="image")),
    ], null=True, blank=True)

    body = StreamField([
        ('heading', blocks.CharBlock(classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('name', classname="full"),
        FieldPanel('acronym', classname="full"),
        FieldPanel('status', classname="full"),
        FieldPanel('status_color', classname="full"),
        FieldPanel('description', classname="full"),
        FieldPanel('sidebar', classname="full"),
    ]

    gallery_panel = [
        StreamFieldPanel('gallery'),
    ]

    specs_panel = [
        ImageChooserPanel('schematic'),
        StreamFieldPanel('body'),
    ]
    snippet_panel = [
        FieldPanel('snippet', classname='full'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(specs_panel, heading='Specs'),
        ObjectList(snippet_panel, heading='Snippet'),
        ObjectList(gallery_panel, heading='Photo Gallery'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])


class UserGuidePage(Page):
    icon = models.CharField(max_length=255, blank=True, )
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('icon', classname="full"),
        StreamFieldPanel('body'),
    ]

    subpage_types = ['UserGuidePage']

    def user_guide_main(self, inclusive=True):
        return Page.objects.ancestor_of(self, inclusive).type(UserGuidePage).order_by('depth').first().specific


class PublicationsPage(RoutablePageMixin, Page):
    api = models.URLField(blank=True)
    acronym = models.CharField(max_length=255, blank=True, )

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)

    kind = 'article'

    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('api', classname="full"),
        FieldPanel('acronym', classname="full"),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(PublicationsPage, self).get_context(request, *args, **kwargs)
        rc = requests.get("{}/categories/{}".format(self.api, self.acronym))
        if rc.status_code == requests.codes.ok:
            categories = rc.json()
            category = [c for c in categories if c['kind'] == self.kind][0]

            rp = requests.get("{}/publications/{}/{}".format(self.api, category['kind'], self.acronym))
            if rp.status_code == requests.codes.ok:
                yr_list = list(reversed(sorted(set([d['date'][:4] for d in rp.json()]))))
                pub_list = [(yr, [d['cite'] for d in rp.json() if yr in d['date']]) for yr in yr_list]
                context.update({
                    'year_list': yr_list,
                    'publication_list': pub_list,
                    'category': category['display'],
                    'categories': categories
                })
        return context

    @route(r'^category/(?P<category>[-\w]+)/$')
    def publications_by_category(self, request, category, *args, **kwargs):
        self.kind = category
        return render(request, "beamlines/blocks/publications.html", self.get_context(request, *args, **kwargs) )


class EmbedPage(Page):
    embed = models.URLField(blank=True)
    height = models.IntegerField(blank=True, null=True, help_text="Height of target page, in pixels")

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)

    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('embed', classname="full"),
        FieldPanel('height', classname="full"),
        StreamFieldPanel('body'),
    ]


class BeamlineDisplayPage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ], blank=True)
    background_url = models.URLField(blank=True)
    gallery = StreamField([
        ('image', ImageChooserBlock(icon="image")),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('background_url', classname="full"),
        StreamFieldPanel('body'),
        StreamFieldPanel('gallery'),
    ]

    def news(self):
        return PostPage.objects.filter(highlight=True).order_by('date')