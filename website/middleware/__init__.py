from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import Http404
import re

INTERNAL_URLS = getattr(settings, 'INTERNAL_URLS', [])
CLIENT_ADDRESS_INDEX = getattr(settings, 'INTERNAL_PROXIES', 1)

def get_client_address(request):
    print "--------------------------"
    print "PROXY", request.META.get('HTTP_X_FORWARDED_FOR','')
    print "REMOTE_ADDR", request.META.get('REMOTE_ADDR')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR','').split(',')
    if len(x_forwarded_for) >= CLIENT_ADDRESS_INDEX:
        ip = x_forwarded_for[-CLIENT_ADDRESS_INDEX]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print "REAL IP", ip
    print "--------------------------"
    return ip


class InternalAccessMiddleware(object):
    """
    Middleware to prevent access to the admin if the user IP
    isn't in the INTERNAL_IPS setting.
    """
    def process_request(self, request):
        if INTERNAL_URLS and any(re.match(addr, request.path) for addr in INTERNAL_URLS):
            if get_client_address(request) in settings.INTERNAL_IPS:
                return 
            else:
                raise Http404()