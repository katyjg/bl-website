from django.conf import settings
from django import template
from django.utils.html import format_html_join, mark_safe

register = template.Library()

import requests


@register.simple_tag
def recent_publications():
    r = requests.get('{}publications/{}/latest/'.format(settings.USO_API, settings.BEAMLINE_ACRONYM))
    if r.status_code == requests.codes.ok:
        pub_list = [d['cite'] for d in r.json()['results']]
    else:
        pub_list = []

    return format_html_join("\n", "<li>{0}</li>", ((mark_safe(p), i) for i, p in enumerate(pub_list)))
