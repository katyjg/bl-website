from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.conf import settings
import re
import mimetypes
from datetime import datetime, timedelta
from django.contrib.humanize.templatetags import humanize

register = template.Library()


@register.simple_tag(takes_context=True)
def site_name(context, *args, **kwargs):
    return getattr(settings, "SITE_NAME_SHORT", "Simple")

@register.filter(name="issue_icon", needs_autoescape=True)
def issue_icon(issue, autoescape=None):
    ICONS = {
        'bug': '<i class="fa fa-bug fa-fw"></i>',
        'task': '<i class="fa fa-tasks fa-fw"></i>',
        'enhancement':'<i class="fa fa-fire fa-fw"></i>',
        'maintenance':'<i class="fa fa-heartbeat fa-fw"></i>',
    }
    icon = ICONS.get(issue.kind, '')
    print icon
    return mark_safe(icon)

@register.filter(name="state_icon", needs_autoescape=True)
def state_icon(issue, autoescape=None):
    ICONS = {
        'new': '<i class="fa fa-start fa-fw fa-3"></i>',
        'pending': '<i class="fa fa-wrench fa-fw fa-3"></i>',
        'started':'<i class="fa fa-cogs fa-fw fa-3"></i>',
        'fixed':'<i class="fa fa-check fa-fw fa-3"></i>',
        'wontfix':'<i class="fa fa-times fa-fw fa-3"></i>',
        'permanent':'<i class="fa fa-thumb-tack fa-fw fa-3"></i>',
    }
    icon = ICONS.get(issue.status, '')
    return mark_safe(icon)

@register.filter(name="file_icon", needs_autoescape=True)
def file_icon(fileobj, autoescape=None):
    ICONS = {
        'pdf': '<i class="fa fa-file-pdf-o fa-fw text-danger"></i>',
        'png': '<i class="fa fa-file-photo-o  fa-fw text-success"></i>',
        'jpeg': '<i class="fa fa-file-photo-o  fa-fw text-info"></i>',
        'gif': '<i class="fa fa-file-photo-o  fa-fw text-warning"></i>',
        'plain': '<i class="fa fa-file-text-o fa-fw"></i>'
    }
    file_type = mimetypes.guess_type(fileobj.path)[0].split('/')[-1]
    icon = ICONS.get(file_type, '<i class="fa fa-file-o"></i>')
    return mark_safe(icon)

@register.filter(name="msg_type", needs_autoescape=True)
def msg_type(tag, autoescape=None):
    TAG = {
        'debug': 'alert',
        'info': 'information',
        'success':'success',
        'warning':'warning',
        'error': 'error',
    }    
    return TAG.get(tag, 'alert')

@register.filter(name="msg_compose", needs_autoescape=True)
def msg_compose(msg, autoescape=None):
    text = '<div class="activity-item">{0}<div class="activity">{1}</div></div>'.format(msg_icon(msg.tags), msg)  
    return mark_safe(text)

@register.filter(name="alarm", needs_autoescape=True)
def alarm(d, autoescape=None):
    if d:
        urgent = (d <= datetime.today().date() and 'Critical') or d <= (datetime.today() + timedelta(days=7)).date() and 'High' or "" 
        return mark_safe("<span class='{0}' title='Due {1}'><i class='fa fa-{2} fa-3'></i></span>".format(urgent, humanize.naturalday(d), 
                                                                                                   urgent and (urgent == 'Critical' and 'exclamation-circle' or 'warning') or 'clock-o' ))
    return d

@register.filter(name="kind_stat")
def kind_stat(issues, kind):
    if issues.exclude(kind__exact="maintenance").count():
        return 100 * (issues.filter(kind__exact=kind).count() / float(issues.exclude(kind__exact='maintenance').count()))
    return 0
    

CONSONANT_SOUND = re.compile(r'''
one(![ir])
''', re.IGNORECASE|re.VERBOSE)
VOWEL_SOUND = re.compile(r'''
[aeio]|
u([aeiou]|[^n][^aeiou]|ni[^dmnl]|nil[^l])|
h(ier|onest|onou?r|ors\b|our(!i))|
[fhlmnrsx]\b
''', re.IGNORECASE|re.VERBOSE)

@register.filter
@stringfilter
def an(text):
    """
    Guess "a" vs "an" based on the phonetic value of the text.

    "An" is used for the following words / derivatives with an unsounded "h":
    heir, honest, hono[u]r, hors (d'oeuvre), hour

    "An" is used for single consonant letters which start with a vowel sound.

    "A" is used for appropriate words starting with "one".

    An attempt is made to guess whether "u" makes the same sound as "y" in
    "you".
    """
    text = force_unicode(text)
    if not CONSONANT_SOUND.match(text) and VOWEL_SOUND.match(text):
        return u'an {0}'.format(text)
    return u'a {0}'.format(text)