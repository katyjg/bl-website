from django.conf.urls import url
import views
import views_attachments

urlpatterns = [
    url(r'^$', views.root_redirect, name='wiki_root'),
    url(r'^([a-zA-Z\d/_-]*)/_edit/$', views.edit, name='wiki_edit'),
    url(r'^([a-zA-Z\d/_-]*)/_create/$', views.create, name='wiki_create'),
    url(r'^([a-zA-Z\d/_-]*)/_history/([0-9]*)/$', views.history, name='wiki_history'),
    url(r'^([a-zA-Z\d/_-]*)/_random/$', views.random_article, name='wiki_random'),
    url(r'^([a-zA-Z\d/_-]*)/_search/articles/$', views.search_articles, name='wiki_search_articles'),
    url(r'^([a-zA-Z\d/_-]*)/_search/related/$', views.search_add_related, name='search_related'),
    url(r'^([a-zA-Z\d/_-]*)/_related/add/$', views.add_related, name='add_related'),
    url(r'^([a-zA-Z\d/_-]*)/_related/remove/(\d+)$', views.remove_related, name='wiki_remove_relation'),
    url(r'^([a-zA-Z\d/_-]*)/_add_attachment/$', views_attachments.add_attachment, name='add_attachment'),
    url(r'^([a-zA-Z\d/_-]*)/_view_attachment/(.+)?$', views_attachments.view_attachment, name='wiki_view_attachment'),
    url(r'^([a-zA-Z\d/_-]*)$', views.view, name='wiki_view'),
    url(r'^(.*)$', views.encode_err, name='wiki_encode_err')
]
