""" Customizing your site:
    1. Save this file as settings_local.py
    2. Update settings_local.py with your information
    3. With the admin file manager, go to the site-images folder and replace the 
       images for:
        - header.png (the header background)
        - overlay.png (the header overlay, if you want one)
        - logo.png (your logo)
        - wiki_logo.png (the logo for your wiki) 
       Each image should be 88px high, with whatever width you want.
"""

import os

# Some meta-data about your site
URL_ROOT = 'http://cmcf.lightsource.ca'
SITE_NAME_LONG = 'Some Beamline Name in Full'
SITE_NAME_SHORT = 'SOME-BL'
SITE_DESCRIPTION = 'A tagline about some beamline'
SITE_KEYWORDS = 'lightsource,canadian,cls,some-keywords-for-your-beamline'

# This should be the acronym assigned to your beamline in the User Office Software
BEAMLINE_ACRONYM = "some-bl"
DEBUG = False

# Recaptcha keys can be obtained at http://www.google.com/recaptcha
RECAPTCHA_PUBLIC_KEY = '6LegXtwSAAAAAN3Xy2oy3hQhSiMuqC8FS4HbXIC_' 
RECAPTCHA_PRIVATE_KEY = '6LegXtwSAAAAAAHw-BviXORo-QXZvU7e7jMtZNba'

# Google custom search engines can be created at https://cse.google.ca/cse/.
# If you want a custom search engine, add a line: GCSE_ID = "your Search engine ID"
#GCSE_ID = "010203040506070809010:abcde123fgh"

# Google analytics can be set up at https://www.google.com/analytics
# If you want to track your site using google analytics, add a line:
# GA_ID = "the site ID listed after your site"
#GA_ID = "UA-12345678-9"

# Django house-keeping stuff specific to your site
########################################################################################################

# Set DEBUG to False when your website is ready for the public
#DEBUG = False

# Set the SECRET_KEY to a unique, unpredictable value
SECRET_KEY = '^a-random-string-with-letters-numbers-and-characters!'

# If you want a different database than the default sqlite one the configuration once you have a mysql database set up.
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'db-name',
#        'USER': 'db-user',
#        'PASSWORD': 'db-passwd',
#        'HOST': 'db-ipaddr',
#        'PORT': ''
#        }
#    }

# Specify how emails from the web server should be sent/received
SERVER_EMAIL = 'bl-web@no-reply.ca' # This just needs to have the form of an email address
EMAIL_SUBJECT_PREFIX = 'Web:'

#ADMINS will receive feedback from the website and 500 errors if they arise
ADMINS = (
    ('TestUser', 'test.user@lightsource.ca'),
)

#SCHEDULERS will receive e-mail notifications about schedule changes
SCHEDULERS = (
    ('TestUser', 'test.user@lightsource.ca'),
    ('CLS Users Office', 'clsuo@lightsource.ca'),
)
AUTO_SCHEDULERS = (
    ('TestUser', 'test.user@lightsource.ca'),
)
CC_AUTO_SCHEDULERS = ()


# The following is only necessary if you have included 'application_form' in the list of INSTALLED_APPS.
########################################################################################################
 
# MANAGERS will receive online application forms
MANAGERS = (
    ('TestUser', 'test.user@lightsource.ca'),
)
# Sender for application_form emails
FROM_EMAIL = 'test.user@lightsource.ca' # This should be an email that exists

# CONF_MANAGERS will receive PSFaM registration forms
CONF_MANAGERS = (
    ('TestUser', 'test.user@lightsource.ca'),
) 
# Sender email for PSFaM Registrations
CONF_FROM_EMAIL = 'test.user@lightsource.ca'
 
