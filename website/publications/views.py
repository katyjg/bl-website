# Create your views here.
from django.shortcuts import render_to_response
from django.conf import settings

import requests

def categories_list():
    r = requests.get('%scategories/%s/' % (settings.USO_API, settings.USO_BEAMLINE))
    if r.status_code == requests.codes.ok:
        return sorted([c['kind'] for c in r.json()])
    else:
        return False

def publication_list(request, **kwargs):
    category = kwargs.get('category','article')
    r = requests.get('%spublications/%s/%s/' % (settings.USO_API, category, settings.USO_BEAMLINE))
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
            'category': category.replace('_',' '),
            'categories': categories_list()},)

def publications_brief(request):
    r = requests.get('%spublications/%s/latest/' % (settings.USO_API, settings.USO_BEAMLINE))
    if r.status_code == requests.codes.ok:
        pub_list = [d['cite'] for d in r.json()['results']]
    else:
        pub_list = []
        print r.status_code

    return render_to_response(
        'publications/publications_brief.html', 
        {'publication_list': pub_list,}, 
        )

