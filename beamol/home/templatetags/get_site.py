from django import template

from wagtail.models import Site

register = template.Library()


@register.simple_tag
def get_site():
    home = Site.objects.first().root_page.specific
    return home
