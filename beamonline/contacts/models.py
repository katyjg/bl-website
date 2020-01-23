from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class PersonnelBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    name = blocks.TextBlock()
    position = blocks.TextBlock(required=False)
    email = blocks.EmailBlock(required=False)
    phone = blocks.TextBlock(required=False)
    office = blocks.TextBlock(required=False)

    class Meta:
        icon = 'user'
        template='contacts/blocks/person.html'

class ContactsPage(Page):
    personnel = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('person', blocks.ListBlock(PersonnelBlock(), icon="user")),
    ], null=True, blank=True)

    sidebar = RichTextField(blank=True)

    personnel_panel = Page.content_panels + [
        StreamFieldPanel('personnel', classname="full"),
    ]

    sidebar_panel = [
        FieldPanel('sidebar', classname="full"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(personnel_panel, heading='Personnel'),
        ObjectList(sidebar_panel, heading='Sidebar'),
        ObjectList(Page.promote_panels, heading='Promote'),
        ObjectList(Page.settings_panels, heading='Settings', classname="settings"),
    ])
