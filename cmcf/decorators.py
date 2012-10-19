from django.http import Http404
from django.conf import settings

import ipaddr
from ipaddr import IPNetwork, IPAddress

from settings import INTERNAL_IPS, ALLOWED_NETWORKS

'''
To hide a view from external ips, just add "from decorators import protectview"
to the top of the views.py, and insert "@protectview" immediately before the view definition.

To allow an IP address to see that view, add it to "INTERNAL_IPS" in the project settings.
'''

def protectview(func):
    def decorator(request,*args,**kwargs):
        for network in ALLOWED_NETWORKS:
            if IPAddress(request.META['REMOTE_ADDR']) in IPNetwork(network):
                return func(request,*args,**kwargs)
        for ip in INTERNAL_IPS:
            if IPAddress(request.META['REMOTE_ADDR']) == IPAddress(ip):
                return func(request,*args,**kwargs)
        raise Http404()
    return decorator
