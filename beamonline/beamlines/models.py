from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks

from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock


table_options = {
    'contextMenu': [
       'row_above',
       'row_below',
       '---------',
       'col_left',
       'col_right',
       '---------',
       'remove_row',
       'remove_col',
       '---------',
       'alignment',
       'undo',
       'redo'
    ],
}

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
    sidebar = RichTextField(blank=True)
    schematic = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='+')
    status = models.CharField(max_length=255, blank=True)
    status_color = models.CharField(max_length=255, choices=STATUS_COLORS)
    gallery = StreamField([
        ('image', blocks.ListBlock(ImageCarouselBlock(), template='beamlines/blocks/carousel.html', icon="image")),
    ], null=True, blank=True)

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('table', TableBlock(table_options=table_options)),
        ('image', ImageChooserBlock(icon="image")),
        ('embedded_video', EmbedBlock(icon="media")),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('name', classname="full"),
        FieldPanel('acronym', classname="full"),
        FieldPanel('status', classname="half"),
        FieldPanel('status_color', classname="half"),
        FieldPanel('description', classname="full"),
        FieldPanel('sidebar', classname="full"),
        ImageChooserPanel('schematic'),
    ]

    gallery_panel = [
        StreamFieldPanel('gallery', classname="full"),
    ]

    specs_panel = [
        StreamFieldPanel('body', classname="full"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(specs_panel, heading='Body'),
        ObjectList(gallery_panel, heading='Photo Gallery'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
