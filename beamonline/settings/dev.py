from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2&427%cz@7e&!x32^wd#pf&^5up3(knp@6^4+psd=hdll$qfk^'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1',]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SITE_NAME_LONG = 'Canadian Macromolecular Crystallography Facility'
SITE_DESCRIPTION = ''
SITE_KEYWORDS = ''
SITE_NAME_SHORT = 'CMCF'
BEAMLINE_ACRONYM = 'CMCF'
ORG_URL = "https://www.lightsource.ca"
ORGANIZATION = "Canadian Light Source, Inc."
USO_API = "http://user-portal.lightsource.ca/api/v1/"

try:
    from .local import *
except ImportError:
    pass
