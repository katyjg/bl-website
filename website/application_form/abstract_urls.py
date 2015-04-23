from django.conf.urls import *

from application_form.views import abstract_list

urlpatterns = patterns('',
   url(r'^$', abstract_list, {'template': 'application_form/abstract_list.html' }, name='abstract_list')
   )
