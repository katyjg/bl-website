from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.conf import settings
from blog.models import Post
from photologue.models import Photo

def news_slider(request):
    post_list = []
    i = 0
    for post in Post.objects.all():
        if i <= -1:
            post_list.append(post)
            i = i+1
        elif post.highlight:
            post_list.append(post)
    for photo in Photo.objects.all():
        if photo.photo_highlight:
            post_list.append(photo)

    return render_to_response(
        'slider/highlights.html', 
        {'news_list': post_list},
        )



