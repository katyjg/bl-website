# Create your views here.
import datetime
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic import date_based, list_detail
from django.db.models import Q
from django.db.models import Count
from django.conf import settings
from publications.models import *
from scheduler.models import Beamline
from tagging.models import Tag, TaggedItem
from scheduler.views import staff_login_required

import string
from string import *

from django.db.models import Q

from django.views.generic.list_detail import object_list
from django.db import connection, transaction

@staff_login_required
def admin_publication_stats(request, template='publications/publications_stats.html'):
    pubs = Publication.objects.all().annotate(num_bls=Count('beamline')).order_by('-journal__impact_factor','-year','-month')
    stats = {'pubs': {}, 'pdbs': {},}
    bls = Beamline.objects.all()
    for key, val in stats.items():
        for k in ['multi','unknown','total','cumulative']:
            stats[key][k] = {}
        for bl in bls:
            stats[key][bl.name] = {}
    
    first_year = Publication.objects.all().order_by('year')[0].year
    last_year = Publication.objects.all().order_by('-year')[0].year
    
    for year in range(first_year, last_year+1):
        ypub = pubs.filter(year__exact=year)
        stats['pubs']['total'][year] = ypub.count()
        stats['pubs']['cumulative'][year] = pubs.filter(year__lte=year).count()
        stats['pubs']['multi'][year] = ypub.filter(num_bls__gt=1).count()
        stats['pubs']['unknown'][year] = ypub.filter(num_bls__exact=0).count()
        stats['pdbs']['total'][year] = sum(len(p.get_pdbs()) for p in ypub)
        stats['pdbs']['cumulative'][year] = stats['pdbs']['total'][year] + (stats['pdbs']['cumulative'].has_key(year-1) and stats['pdbs']['cumulative'][year-1] or 0)
        stats['pdbs']['unknown'][year] = sum(len(p.get_pdbs()) for p in ypub.exclude(num_bls__exact=1))
        stats['pdbs']['multi'][year] = 0
        for bl in bls:
            stats['pubs'][bl.name][year] = ypub.filter(beamline__exact=bl).count()
            stats['pdbs'][bl.name][year] = sum(len(p.get_pdbs()) for p in ypub.filter(num_bls__exact=1).filter(beamline__exact=bl))

    return render_to_response(template, { 'title': 'Publication Statistics',
                                          'admin': True,
                                          'publications': pubs,
                                          'stats': stats,
                                          'categories': {'pubs': 'Publications', 'pdbs': 'PDB Releases'},
                                          'beamlines': [bl.name for bl in bls],
                                          'extra_rows': ['unknown','total'],
                                          'plots': ['total','cumulative'],
                                         },
                              )

@staff_login_required
def admin_pub_table(request, field, template='publications/publication_table.html'):
    pubs = Publication.objects.all().annotate(num_bls=Count('beamline')).order_by('-'+field,'-year','-month')
    return render_to_response(template, {  'admin': True,
                                           'publications': pubs,
                                         }, context_instance=None)
     
def publications_brief(request):
    pub_list = []
    author_list = []
    data_list = []
    i = 0
    for publication in sorted(Publication.objects.all(), key=lambda Publication: Publication.created, reverse=True):
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
    for publication in sorted(Publication.objects.all(), key=lambda Publication: Publication.authors.split(',')[0].split(' ')[-1]):
        data_list = []
        data_list.append(publication)
        data_list.append(publication.pdb_entries.split(','))
        pub_list.append(data_list)

    return object_list(request, 
                        queryset=Publication.objects.all(), 
                        extra_context={ 'publication_list': pub_list,
                                        'year_list': year_list},
                        **kwargs)
    
def poster_list(request, **kwargs):
    poster_list = Poster.objects.all()
    return object_list(request, 
                        queryset=Poster.objects.all(), 
                        extra_context={ 'poster_list': poster_list },
                        **kwargs)
    
