import datetime
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic.list import ListView

from django.db.models import Q
from django.conf import settings
from blog import models
from photologue.models import Photo

def post_list(request):
    category = []
    # This can be fixed up with Django >= 1.3 (.values(<ManytoManyField>) won't give an error then)
    for post in models.Post.objects.all():
        for cat in post.categories.all():
            if cat not in category:
                category.append(cat)

    return render_to_response(
        'blog/post_list.html', 
        {
            'object_list': models.Post.objects.all(),
            'categories': category,
        },
        )

def news_slider(request):
    post_list = []
    i = 0
    for post in models.Post.objects.all():
        if i <= -1:
            post_list.append(post)
            i = i+1
        elif post.highlight:
            post_list.append(post)
    for photo in Photo.objects.all():
        if photo.photo_highlight:
            post_list.append(photo)

    return render_to_response(
        'blog/highlights.html', 
        {'news_list': post_list},
        )

def news_brief(request):
    post_list = []
    i = 0
    for post in models.Post.objects.all():
        if i <= 4:
            post_list.append(post)
            i = i+1
    return render_to_response(
        'blog/news_brief.html', 
        {'post_list': post_list},
        )

def category_detail(request, slug, template_name = 'blog/category_detail.html', **kwargs):
    """
    Category detail

    Template: ``blog/category_detail.html``
    Context:
        object_list
            List of posts specific to the given category.
        category
            Given category.
    """
    category_list = []
    # This can be fixed up with Django >= 1.3 (.values(<ManytoManyField>) won't give an error then)
    for post in models.Post.objects.all():
        for cat in post.categories.all():
            if cat not in category_list:
                category_list.append(cat)
                
    category = get_object_or_404(models.Category, slug__iexact=slug)

    return render_to_response(
        template_name, 
        {
            'object_list': category.post_set.all(),
            'categories': category_list,
            'category': category
        },
        )
    

# Stop Words courtesy of http://www.dcs.gla.ac.uk/idom/ir_resources/linguistic_utils/stop_words
STOP_WORDS = r"""\b(a|about|above|across|after|afterwards|again|against|all|almost|alone|along|already|also|
although|always|am|among|amongst|amoungst|amount|an|and|another|any|anyhow|anyone|anything|anyway|anywhere|are|
around|as|at|back|be|became|because|become|becomes|becoming|been|before|beforehand|behind|being|below|beside|
besides|between|beyond|bill|both|bottom|but|by|call|can|cannot|cant|co|computer|con|could|couldnt|cry|de|describe|
detail|do|done|down|due|during|each|eg|eight|either|eleven|else|elsewhere|empty|enough|etc|even|ever|every|everyone|
everything|everywhere|except|few|fifteen|fify|fill|find|fire|first|five|for|former|formerly|forty|found|four|from|
front|full|further|get|give|go|had|has|hasnt|have|he|hence|her|here|hereafter|hereby|herein|hereupon|hers|herself|
him|himself|his|how|however|hundred|i|ie|if|in|inc|indeed|interest|into|is|it|its|itself|keep|last|latter|latterly|
least|less|ltd|made|many|may|me|meanwhile|might|mill|mine|more|moreover|most|mostly|move|much|must|my|myself|name|
namely|neither|never|nevertheless|next|nine|no|nobody|none|noone|nor|not|nothing|now|nowhere|of|off|often|on|once|
one|only|onto|or|other|others|otherwise|our|ours|ourselves|out|over|own|part|per|perhaps|please|put|rather|re|same|
see|seem|seemed|seeming|seems|serious|several|she|should|show|side|since|sincere|six|sixty|so|some|somehow|someone|
something|sometime|sometimes|somewhere|still|such|system|take|ten|than|that|the|their|them|themselves|then|thence|
there|thereafter|thereby|therefore|therein|thereupon|these|they|thick|thin|third|this|those|though|three|through|
throughout|thru|thus|to|together|too|top|toward|towards|twelve|twenty|two|un|under|until|up|upon|us|very|via|was|
we|well|were|what|whatever|when|whence|whenever|where|whereafter|whereas|whereby|wherein|whereupon|wherever|whether|
which|while|whither|who|whoever|whole|whom|whose|why|will|with|within|without|would|yet|you|your|yours|yourself|
yourselves)\b"""


def search(request, template_name='blog/post_search.html'):
    """
    Search for blog posts.

    This template will allow you to setup a simple search form that will try to return results based on
    given search strings. The queries will be put through a stop words filter to remove words like
    'the', 'a', or 'have' to help imporve the result set.

    Template: ``blog/post_search.html``
    Context:
        object_list
            List of blog posts that match given search term(s).
        search_term
            Given search term.
    """
    context = {}
    if request.GET:
        stop_word_list = re.compile(STOP_WORDS, re.IGNORECASE)
        search_term = '%s' % request.GET['q']
        cleaned_search_term = stop_word_list.sub('', search_term)
        cleaned_search_term = cleaned_search_term.strip()
        if len(cleaned_search_term) != 0:
            post_list = models.Post.objects.published().filter(Q(title__icontains=cleaned_search_term) | Q(body__icontains=cleaned_search_term) | Q(tags__icontains=cleaned_search_term) | Q(categories__title__icontains=cleaned_search_term))
            context = {'object_list': post_list, 'search_term':search_term}
        else:
            message = 'Search term was too vague. Please try again.'
            context = {'message':message}
    return render_to_response(template_name, context, context_instance=RequestContext(request))
