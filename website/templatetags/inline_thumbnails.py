import re

from django import template
from django.template.defaultfilters import stringfilter

from sorl.thumbnail.main import DjangoThumbnail

from models import InlineImage

register = template.Library()

regex = re.compile(r'\[thumbnail (?P<identifier>[\-\w]+)\]')


@register.filter
@stringfilter
def inline_thumbnails(value):
    new_value = value
    it = regex.finditer(value)
    for m in it:
        try:
            image = InlineImage.objects.get(identifier=identifier)
            thumbnail = DjangoThumbnail(image.image, (500, 500))
            new_value = new_value.replace(m.group(), '<img src="%s%s" width="%d" height="%d" alt="%s" /><p><em>%s</em></p>' % ('http://mysite.com', thumbnail.absolute_url, thumbnail.width(), thumbnail.height(), image.title, image.title))
        except InlineImage.DoesNotExist:
            pass
    return new_value

