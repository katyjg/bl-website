# Create your views here.
from django.shortcuts import render_to_response
from django.conf import settings

import requests

def categories_list():
    r = requests.get('%scategories/%s/' % (settings.USO_API, settings.BEAMLINE_ACRONYM))
    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        return False

def publication_list(request, **kwargs):
    categories = categories_list()
    category = [c for c in categories if c['kind'] == kwargs.get('category','article')][0]
    r = requests.get('%spublications/%s/%s/' % (settings.USO_API, category['kind'], settings.BEAMLINE_ACRONYM))
    if r.status_code == requests.codes.ok:
        yr_list = list(reversed(sorted(set([d['date'][:4] for d in r.json()]))))
        pub_list = [(yr, [d['cite'] for d in r.json() if yr in d['date']]) for yr in yr_list]
    else:
        yr_list = []
        pub_list = []
        print r.status_code

    return render_to_response(
        'publications/publication_list.html', 
        {  
            'year_list': yr_list,
            'publication_list': pub_list, 
            'category': category['display'],
            'categories': categories},)

def publications_brief(request):
    r = requests.get('{}publications/{}/latest/'.format(settings.USO_API, settings.BEAMLINE_ACRONYM))
    if r.status_code == requests.codes.ok:
        pub_list = [d['cite'] for d in r.json()['results']][:3]
    else:
        pub_list = []

    return render_to_response(
        'publications/publications_brief.html', 
        {'publication_list': pub_list,}, 
        )

