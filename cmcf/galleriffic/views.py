# Create your views here.
from photologue.models import *
import os
import random
import shutil
import zipfile

from datetime import datetime
from inspect import isclass

from django.db import models
from django.db.models.signals import post_init
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.functional import curry
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404

# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    import Image
    import ImageFile
    import ImageFilter
    import ImageEnhance
except ImportError:
    try:
        from PIL import Image
        from PIL import ImageFile
        from PIL import ImageFilter
        from PIL import ImageEnhance
    except ImportError:
        raise ImportError('Photologue was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')

def gallery_display(request, slug):
    photo_list = []
    for photo in Photo.objects.all():
	if slug == '08id1' and photo.gallery == 1:
	    photo.galleryname = "08ID-1 Construction"
	    photo_list.append(photo)
	elif slug == '08b1' and photo.gallery == 2:
	    photo.galleryname = "08B1-1 Construction"
	    photo_list.append(photo)

    return render_to_response(
        'galleriffic/gallery_display.html', 
        {'gallery_list': photo_list}
        )

def all_display(request):
    photo_list = []
    for photo in Photo.objects.all():
        photo.galleryname = "All Images"
	photo_list.append(photo)

    return render_to_response(
        'galleriffic/gallery_display.html', 
        {'gallery_list': photo_list}
        )

