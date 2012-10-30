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
    pubs = Publication.objects.all().order_by('-journal__impact_factor','-publish')
    stats = {}
    bls = Beamline.objects.all()
    for key in ['norm','add','bls']: stats[key] = { 'pubs': {}, 'pdbs': {},}
    for bl in bls:
        for key in ['pubs','pdbs']:
            stats['bls'][key][bl.name] = {}
            stats['bls'][key]['multi'] = {}
    for p in Publication.objects.all().order_by('year'):
        if not stats['norm']['pubs'].has_key(p.year):
            for key in ['pubs','pdbs']: 
                for bl in bls:
                    stats['bls'][key][bl.name][p.year] = 0
                    stats['bls'][key]['multi'][p.year] = 0
                stats['norm'][key][p.year] = 0
            for pub in Publication.objects.filter(year__exact=p.year):
                stats['norm']['pubs'][p.year] += 1
                for bl in pub.get_beamlines().split(','):
                    stats['bls']['pubs'][bl][p.year] += 1
                if len(pub.get_beamlines().split(',')) > 1:
                    stats['bls']['pubs']['multi'][p.year] += 1
                if pub.get_pdbs() != ['']: 
                    stats['norm']['pdbs'][p.year] += len(pub.get_pdbs())
                    for bl in pub.get_beamlines().split(','):
                        stats['bls']['pdbs'][bl][p.year] += len(pub.get_pdbs())
                    if len(pub.get_beamlines().split(',')) > 1:
                        stats['bls']['pdbs']['multi'][p.year] += len(pub.get_pdbs())
            for key in ['pubs','pdbs']:
                last_year = ( stats['add'][key].has_key(p.year-1) and stats['add'][key][p.year-1] ) or 0
                stats['add'][key][p.year] = stats['norm'][key][p.year] + last_year 
    
    return render_to_response(template, { 'title': 'Publication Statistics',
                                          'admin': True,
                                          'publications': pubs,
                                          'stats': stats,
                                          'categories': {'pubs': 'Publications', 'pdbs': 'PDB Releases'}
                                         },
                              )

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
    
def poster_list(request, **kwargs):
    poster_list = Poster.objects.all()
    return object_list(request, 
                        queryset=Poster.objects.all(), 
                        extra_context={ 'poster_list': poster_list },
                        **kwargs)
    