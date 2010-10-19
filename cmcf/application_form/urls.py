from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from application_form.views import application_form, applicant_list

urlpatterns = patterns('',
                       url(r'^$',
                           application_form,
                           name='application_form'),
                       url(r'^sent/$',
                           direct_to_template,
                           { 'template': 'application_form/application_form_sent.html' },
                           name='application_form_sent'),
                       url(r'^oops/$',
                           direct_to_template,
                           { 'template': 'application_form/application_form_retry.html' },
                           name='application_form_retry'),
                       url(r'^applicant_list/$',
                           applicant_list,
                           name='applicant_list'),
                       )
