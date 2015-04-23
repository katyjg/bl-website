from django.conf.urls import *
from django.views.generic import TemplateView

from application_form.views import application_form, applicant_list

urlpatterns = patterns('',
    url(r'^$', application_form, name='application_form'),
    url(r'^sent/$', TemplateView.as_view(template_name='application_form/application_form_sent.html'), name='application_form_sent'),
    url(r'^oops/$', TemplateView.as_view(template_name='application_form/application_form_retry.html'), name='application_form_retry'),
    url(r'^applicant_list/$', applicant_list, name='applicant_list'),
)
