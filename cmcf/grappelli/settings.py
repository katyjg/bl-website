# coding: utf-8

from django.conf import settings

SHORT_NAME = getattr(settings, "SITE_NAME_SHORT", '')

# Admin Site Title
ADMIN_HEADLINE = getattr(settings, "GRAPPELLI_ADMIN_HEADLINE", SHORT_NAME)
ADMIN_TITLE = getattr(settings, "GRAPPELLI_ADMIN_TITLE", SHORT_NAME)

# Link to your Main Admin Site (no slashes at start and end)
ADMIN_URL = getattr(settings, "GRAPPELLI_ADMIN_URL", '/admin/')
