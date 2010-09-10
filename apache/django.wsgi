import os
import sys

sys.path.append('/var/website/cmcf-website')
sys.path.append('/var/website/cmcf-website/cmcf')

os.environ['DJANGO_SETTINGS_MODULE'] = 'cmcf.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

