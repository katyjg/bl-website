from django.core.management.base import BaseCommand, CommandError
from django.core.files.images import ImageFile

from wagtail.images.models import Image

from news.models import NewsPage, PostPage, PostCategory

import json
from io import BytesIO
import requests


class Command(BaseCommand):
    help = 'Imports blog entries from the Django 2 website to news posts.'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **options):
        news_page = NewsPage.objects.live().first()
        blog_file = options['file']
        with open(blog_file) as json_blogs:
            data = json.load(json_blogs)
            posts = [p for p in data if p['model'] == 'blog.post']
            for p in posts:
                fields = p['fields']
                if not PostPage.objects.filter(slug=fields['slug']).exists():
                    if fields['link'] or fields['citation']:
                        body = "{}<a href='{}'>{}</a>".format(fields['body'], fields['link'], fields['citation'])
                    else:
                        body = fields['body']
                    info = {
                        'title': fields['title'],
                        'slug': fields['slug'],
                        'body': body,
                        'subtitle': fields['tease'].replace("<p>", "").replace("</p>","")[:510],
                        'date': fields['publish'].replace("'", "")[:10],
                        'highlight': fields['highlight']
                    }
                    post = PostPage(**info)
                    news_page.add_child(instance=post)
                    for c in fields['categories']:
                        post.categories.add(PostCategory.objects.get(pk=c))

                    r = requests.get('https://cmcf.lightsource.ca/media/{}'.format(fields['image']))
                    if r.status_code == requests.codes.ok:
                        image = Image(title=fields['title'], file=ImageFile(BytesIO(r.content), name=fields['image']))
                        image.save()
                        post.image = image
                        post.save()
