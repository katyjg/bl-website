from django.http import Http404

from cmcf.settings import INTERNAL_IPS

'''
To hide a view from external ips, just add "from cmcf.decorators import protectview"
to the top of the views.py, and insert "@protectview" immediately before the view definition.

To allow an IP address to see that view, add it to "INTERNAL_IPS" in the project settings.
'''

def protectview(func):
    def decorator(request,*args,**kwargs):
        if request.META['REMOTE_ADDR'] not in INTERNAL_IPS:
            raise Http404()
        return func(request,*args,**kwargs)
    return decorator
