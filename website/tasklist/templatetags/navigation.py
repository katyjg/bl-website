from django import template
from django.core import urlresolvers
import re
 
register = template.Library()
 
 
@register.simple_tag(takes_context=True)
def active(context, url_name, *args, **kwargs):
    matches = current_url_equals(context, url_name, *args, **kwargs)
    return 'active' if matches else ''
 
@register.simple_tag(takes_context=True)
def active_root(context, url_name, *args, **kwargs):
    matches = current_url_startswith(context, url_name, *args, **kwargs)
    return 'active' if matches else ''

 
def current_url_equals(context, url_name, *args, **kwargs):
    resolved = False
    try:
        resolved = urlresolvers.resolve(context.get('request').path)
    except:
        pass
    
    matches = resolved and resolved.url_name == url_name
    
    if matches and (args or kwargs):
        if not (set(resolved.kwargs.items()) >= set(kwargs.items())):
            if not (set(args) + set(kwargs.values())) >= (set(kwargs.values()) + set(args)):
                return False
    return matches


def current_url_startswith(context, url_name, *args, **kwargs):
    try:
        reversed = urlresolvers.reverse(url_name, args=args, kwargs=kwargs)
        return context.get('request').path.startswith(reversed)
    except:
        return context.get('request').path.startswith(url_name)
    
