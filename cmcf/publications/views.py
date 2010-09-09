# Create your views here.
import datetime
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic import date_based, list_detail
from django.db.models import Q
from django.conf import settings
from publications.models import *
from tagging.models import Tag, TaggedItem

import string
from string import *

from django.db.models import Q

from django.views.generic.list_detail import object_list
from django.db import connection, transaction

def publications_brief(request):
    pub_list = []
    i = 0
    for publication in Publication.objects.all():
        if i <= 2:
            pub_list.append(publication)
            i = i+1

    return render_to_response(
        'publications/publications_brief.html', 
        {'publication_list': pub_list},
        )

def publication_archive_year(request, year):
    pub_list = []
    for publication in Publication.objects.all():
        if (int(year) == publication.year):
            pub_list.append(publication)

    return render_to_response(
        'publications/publication_list.html', 
        {'publication_list': pub_list}
        )

def publication_list(request, **kwargs):
    publications = Publication.objects.all()
 
    all_years_list = []
    year_list = []
    pub_list = []
    link_list = {}
    for publication in Publication.objects.all():
        pub_list.append(publication)
        all_years_list.append(publication.year)
        if all_years_list.count(publication.year)==1:
            year_list.append(publication.year)
	
    return object_list(request, 
                        queryset=publications, 
                        extra_context={ 'publication_list': pub_list,
                                        'year_list': year_list},
                        **kwargs)
