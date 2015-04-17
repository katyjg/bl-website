from django.conf.urls import *
from django.views.generic import TemplateView

from application_form.views import application_form, applicant_list, participant_list
from application_form.forms import RegistrationForm
from application_form.models import Registration

urlpatterns = patterns('',
   url(r'^$', application_form, {'model': Registration, 'form_class': RegistrationForm, 'template_name': 'application_form/registration_form.html', 'template_retry': 'application_form/registration_form_retry.html', 'success_url': 'registration_form_sent' }, name='registration_form'),
   url(r'^sent/$', TemplateView.as_view(template_name='application_form/registration_form_sent.html'), name='registration_form_sent'),
   url(r'^oops/$', TemplateView.as_view(template_name='application_form/registration_form_retry.html'), name='registration_form_retry'),
   url(r'^706d24997absdjckw325812f81a58e369/$', participant_list, {'template': 'application_form/participant_list.html' }, name='participant_list'),
   url(r'^a5ca37fa4d0856a4176f6355ea2ec888/$', participant_list, {'template': 'application_form/registration_abstract_list.html' }, name='registration_abstract_list'),
)
