from django.conf import settings
from django import template
from django.utils.html import format_html_join, mark_safe

from beamlines.models import PublicationsPage

register = template.Library()

import requests


@register.simple_tag
def publications_page():
    return PublicationsPage.objects.live().first()


@register.simple_tag
def recent_publications(api, acronym):
    r = requests.get('{}/publications/{}/latest/'.format(api, acronym))
    if r.status_code == requests.codes.ok:
        pub_list = [d['cite'] for d in r.json()['results']]
    else:
        pub_list = []

    return format_html_join("\n", "<li>{0}</li>", ((mark_safe(p), i) for i, p in enumerate(pub_list)))


