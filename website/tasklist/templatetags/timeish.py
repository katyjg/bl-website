# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime
import calendar
from django.utils import timezone
from django import template
from django.utils.html import avoid_wrapping

register = template.Library()


@register.filter
def ago(value):
    return timefrom(value)

@register.filter
def remaining(value):
    return timefrom(value, reverse=True, over="overdue")


def timefrom(value, reverse=False, over=""):
    """
    For date and time values shows how many seconds, minutes or hours ago
    compared to current timestamp returns representing string.
    """
    if not isinstance(value, date):  # datetime is a subclass of date
        return value
    chunks = (
        (60 * 60 * 24 * 365, '{0} {1} yr{3} {2}'),
        (60 * 60 * 24 * 30, '{0} {1} mth{3} {2}'),
        (60 * 60 * 24 * 7, '{0} {1} wk{3} {2}'),
        (60 * 60 * 24, '{0} {1} day{3} {2}'),
        (60 * 60, '{0} {1} hr{3} {2}'),
        (60, '{0} {1} min{3} {2}')
    )

    now = timezone.now()
    # Convert datetime.date to datetime.datetime for comparison.
    if not isinstance(value, datetime):
        value = datetime.combine(value, datetime.min.time())
    print now, value
    delta = (value - now) if reverse else (now - value)
    prefix = 'in' if reverse else ''
    suffix = 'ago' if not reverse else '' 
    since = delta.days * 24 * 60 * 60 + delta.seconds
    if since < 0:
        # d is in the future compared to now, stop processing.
        return avoid_wrapping(over)
    elif since < 60:
        return avoid_wrapping('now')
    for (seconds, name) in chunks:
        count = since // seconds
        if count != 0:
            break
    if count > 1:
        plul = 's'
    else:
        plul = ' '
    result = avoid_wrapping(name.format(prefix, count, suffix, plul))
    return result

@register.filter
def age(bday, d=None):
    if d is None:
        d = date.today()
        d = date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])
    return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))
    

