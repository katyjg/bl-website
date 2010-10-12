from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse
from blog.models import Post, Category
from django.utils.feedgenerator import Rss201rev2Feed


class RssFooFeedGenerator(Rss201rev2Feed):
    def add_root_elements(self, handler):
        super(RssFooFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement(u"image", '',
            {
                 'url': u"http://cmcf.lightsource.ca/media/img/clslogo_feed.png",
                 'title': u"Some title",
                 'link': u"http://cmcf.lightsource.ca/", 
             })     

class LatestEntries(Feed):
    feed_type = RssFooFeedGenerator
    _site = Site.objects.get_current()
    description = "Updates from CMCF at the Canadian Light Source."
    title = '%s News' % _site.name
#    description = '%s posts feed.' % _site.name
    link = '/research-highlights/'

    def items(self):
        return Post.objects.published()[:5]

    def item_link(self, item):
        url_link = []
        url_link.append("/research-highlights/#")
        url_link.append(item.slug)
        return ''.join(url_link)

    def item_description(self, item):
        return item.tease

'''     url_link.append(":8000/research-highlights")
        url_link.append(str(item.publish.year))
        url_link.append(item.publish.strftime('%b').lower())
        url_link.append(str(item.publish.day))'''

'''({
            'year': item.publish.year,
            'month': item.publish.strftime('%b').lower(),
            'day': item.publish.day,
            'slug': item.slug
        })
'''

class BlogPostsFeed(Feed):
    _site = Site.objects.get_current()
    title = '%s feed' % _site.name
    description = '%s posts feed.' % _site.name

    def link(self):
        return reverse('blog_index')

    def items(self):
        return Post.objects.published()[:10]

    def item_pubdate(self, obj):
        return obj.publish


class BlogPostsByCategory(Feed):
    _site = Site.objects.get_current()
    title = '%s posts category feed' % _site.name

    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.objects.get(slug__exact=bits[0])

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Posts recently categorized as %s" % obj.title

    def items(self, obj):
        return obj.post_set.published()[:10]

class CommentsFeed(Feed):
    _site = Site.objects.get_current()
    title = '%s comment feed' % _site.name
    description = '%s comments feed.' % _site.name#

    def link(self):
        return reverse('blog_index')

    def items(self):
        ctype = ContentType.objects.get_for_model(Post)
        return Comment.objects.filter(content_type=ctype)[:10]

    def item_pubdate(self, obj):
        return obj.submit_date
