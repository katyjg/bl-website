from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from application_form.views import abstract_list

urlpatterns = patterns('',
   url(r'^$', abstract_list, {'template': 'application_form/abstract_list.html' }, name='abstract_list')
   )
