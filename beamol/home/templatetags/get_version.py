from django.conf import settings
from django import template

register = template.Library()  
 
@register.filter("get_version")  
def get_version(val=None):
    return settings.VERSION
    
@register.filter("get_from_settings")
def get_from_settings(val=None):
    return getattr(settings, val, '')

