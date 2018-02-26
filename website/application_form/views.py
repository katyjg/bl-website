from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils.datastructures import OrderedDict

import datetime
from scheduler.views import staff_login_required
from application_form.forms import ApplicationForm, RegistrationForm
from application_form.models import Application, Registration

from django.views.decorators.csrf import csrf_protect

@csrf_protect
def application_form(request, form_class=ApplicationForm, model=Application,
                 template_name='application_form/application_form.html',
                 template_retry='application_form/application_form_retry.html',
                 success_url='sent', extra_context=None,
                 fail_silently=False):

    success_url = ( success_url or reverse('application_form_sent'))
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, request=request)
        form_dict = {}
        if form.is_valid():
            data = form.cleaned_data
            for field in model._meta.fields:
                if field.name not in ['id','created']:
                    form_dict[field.name] = data.get(field.name,'')

            if form_class == ApplicationForm:
                bools = ['travel','visa','crystals','stay']
                for key in ['travel','visa','crystals','stay']:
                    if data.get(key,'') == 'yes': form_dict[key] = 1
                    else: form_dict[key] = 0
                applicant = Application()
            elif form_class == RegistrationForm:
                bools = ['mixer']
                applicant = Registration()
                if not data.has_key('type'): form_dict['type'] = None

            for key in bools:
                if data.get(key,'') == 'yes': form_dict[key] = 1
                else: form_dict[key] = 0

            for key, val in form_dict.items():
                setattr(applicant, key, val)

            applicant.save()
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
        else:
            return render(request, template_retry,
                                      {'form': form},
                                      )
    else:
        form = form_class(request=request)

    if extra_context is None:
        extra_context = {}
    context = {}
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render(request, template_name,
                              { 'form': form },
                              )

@staff_login_required
def applicant_list(request):
    applicant_list = []
    this_year = datetime.date.today().year
    applicant_list = Application.objects.filter(created__year=this_year).order_by('sup_name','created')

    return render_to_response(
        'application_form/applicant_list.html', 
        {
            'applicant_list': applicant_list,
        },
        )

def participant_list(request, template='application_form/participant_list.html'):
    regs = Registration.objects.exclude(abstract__exact='').order_by('last_name')
    return render_to_response(template,
                              {'present': {'Oral': regs.filter(talk=True), 'Poster': regs.filter(poster=True)},
                               'participant_list': Registration.objects.all().order_by('last_name'),},)

def abstract_list(request, template='application_form/registration_abstract_list.html'):
    regs = Registration.objects.exclude(abstract__exact='')
    return render_to_response(template,
                              {'present': OrderedDict([('Oral',regs.filter(talk=True)), ('Poster',regs.filter(poster=True))]),},)
    
    