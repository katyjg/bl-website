from django.db import models
from django import forms

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag as TaggitTag

import datetime


class NewsPage(RoutablePageMixin, Page):
    description = models.CharField(max_length=255, blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel('description', classname="full")
    ]

    subpage_types = ['PostPage']
    search_type = None

    def get_posts(self):
        posts = PostPage.objects.descendant_of(self).order_by('-date').live()
        if self.get_filters():
            return posts.filter(**{self.search_type: self.search_term})
        return posts

    def get_categories(self):
        categories = PostCategory.objects.filter(pk__in=PostPage.objects.live().values_list('categories', flat=True))
        return categories


    def get_filters(self):
        return self.search_type and {self.search_type: self.search_term} or None

    def get_context(self, request, *args, **kwargs):
        context = super(NewsPage, self).get_context(request, *args, **kwargs)
        context['search_term'] = hasattr(self, 'display_name') and self.display_name or None
        return context

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'categories__slug'
        self.search_term = category
        self.display_name = PostCategory.objects.get(slug=category).name
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tags__slug'
        self.search_term = tag
        self.display_name = tag
        return Page.serve(self, request, *args, **kwargs)


class PostPage(Page):
    subtitle = models.CharField(max_length=510, blank=True)
    body = RichTextField(blank=True)
    date = models.DateField(default=datetime.date.today)
    image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    highlight = models.BooleanField(default=True)
    categories = ParentalManyToManyField('news.PostCategory', blank=True)
    tags = ClusterTaggableManager(through='news.PostTag', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('body', classname="full"),
        FieldPanel('highlight'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
        FieldPanel('date', classname="full"),
        ImageChooserPanel('image'),
    ]

    parent_page_types = ['NewsPage']
    subpage_types = []

    class Meta:
        verbose_name = "News Item"

    def get_context(self, request, *args, **kwargs):
        context = super(PostPage, self).get_context(request, *args, **kwargs)
        context['news_page'] = self.get_parent().specific
        return context


@register_snippet
class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class PostTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name='post_tags')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True