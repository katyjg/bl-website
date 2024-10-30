from wagtail.admin.panels import FieldPanel, TabbedInterface, ObjectList
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock


class PersonnelBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    hover_image = ImageChooserBlock(required=False)
    name = blocks.TextBlock()
    position = blocks.TextBlock(required=False)
    email = blocks.EmailBlock(required=False)
    phone = blocks.TextBlock(required=False)
    office = blocks.TextBlock(required=False)

    class Meta:
        icon = 'user'
        template = 'contacts/blocks/person.html'


class ContactsPage(Page):
    personnel = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('person', blocks.ListBlock(PersonnelBlock(), icon="user")),
    ], use_json_field=True, null=True, blank=True)

    sidebar = RichTextField(blank=True)

    personnel_panel = Page.content_panels + [
        FieldPanel('personnel'),
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
