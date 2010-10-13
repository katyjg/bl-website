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
    author_list = []
    data_list = []
    i = 0
    for publication in Publication.objects.all():
        if i <= 2:
	    data_list = []
	    author_list = publication.authors.split(', ')
	    if len(author_list) is 3:
		authors = author_list[0] + ', ' + author_list[1] + ' and ' + author_list[2]
            elif len(author_list) is 2:
		authors = author_list[0] + ', ' + author_list[1]
	    elif len(author_list) is 1:
		authors = author_list[0]
	    else:
		authors = author_list[0] + ', et al'
	    data_list.append(publication)
	    data_list.append(authors)
            pub_list.append(data_list)
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
    all_years_list = []
    year_list = []
    pub_list = []
    for publication in Publication.objects.all():
	all_years_list.append(publication.year)
        if all_years_list.count(publication.year)==1:
            year_list.append(publication.year)
    for publication in sorted(Publication.objects.all(), key=lambda Publication: Publication.authors.split(',')[0].split(' ')[1].capitalize()):
	data_list = []
	data_list.append(publication)
	data_list.append(publication.pdb_entries.split(','))
        pub_list.append(data_list)
	
    return object_list(request, 
                        queryset=Publication.objects.all(), 
                        extra_context={ 'publication_list': pub_list,
                                        'year_list': year_list},
                        **kwargs)
