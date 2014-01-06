from django.conf.urls import *
from django.views.generic import TemplateView

from contact_form.views import contact_form

urlpatterns = patterns('',
   url(r'^$',
       contact_form,
       name='contact_form'),
   url(r'^sent/$',
       TemplateView.as_view(template_name='contact_form/contact_form_sent.html'),
       name='contact_form_sent'),
)
