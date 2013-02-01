from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from application_form.views import application_form, applicant_list, participant_list
from application_form.forms import RegistrationForm
from application_form.models import Registration

urlpatterns = patterns('',
   url(r'^$', application_form, {'model': Registration, 'form_class': RegistrationForm, 'template_name': 'application_form/registration_form.html', 'template_retry': 'application_form/registration_form_retry.html', 'success_url': 'registration_form_sent' }, name='registration_form'),
   url(r'^sent/$', direct_to_template, { 'template': 'application_form/registration_form_sent.html' }, name='registration_form_sent'),
   url(r'^oops/$', direct_to_template, { 'template': 'application_form/registration_form_retry.html' }, name='registration_form_retry'),
   url(r'^participant-list/$', participant_list, name='participant_list'),
   )
