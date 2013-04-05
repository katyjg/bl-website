from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

import datetime
from scheduler.views import staff_login_required
from application_form.forms import ApplicationForm, RegistrationForm
from application_form.models import Application, Registration

def application_form(request, form_class=ApplicationForm, model=Application,
                 template_name='application_form/application_form.html',
                 template_retry='application_form/application_form_retry.html',
                 success_url=None, extra_context=None,
                 fail_silently=False):

    success_url = ( success_url is None and reverse('application_form_sent') or reverse(success_url) )
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, request=request)
        form_dict = {}
        for field in model._meta.fields:
            if field.name not in ['id','created']:
                form_dict[field.name] = request.POST.get(field.name,'')

        if form_class == ApplicationForm:    
            bools = ['travel','visa','crystals','stay']
            for key in ['travel','visa','crystals','stay']:
                if request.POST.get(key,'') == 'yes': form_dict[key] = 1
                else: form_dict[key] = 0
            applicant = Application()
        elif form_class == RegistrationForm:
            bools = ['talk']
            applicant = Registration()
            if not request.POST.has_key('type'): form_dict['type'] = None
        
        for key in bools:
            if request.POST.get(key,'') == 'yes': form_dict[key] = 1
            else: form_dict[key] = 0

        for key, val in form_dict.items(): 
            setattr(applicant, key, val)

        if form.is_valid():
            applicant.save()
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
        else:
            return render_to_response(template_retry,
                                      {'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = form_class(request=request)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)

@staff_login_required
def applicant_list(request):
    applicant_list = []
    this_year = datetime.date.today().year
    for applicant in Application.objects.filter(created__year=this_year).order_by('created'):
        applicant_list.append(applicant)

    return render_to_response(
        'application_form/applicant_list.html', 
        {
            'applicant_list': applicant_list,
        },
        )

def participant_list(request, template='application_form/participant_list.html'):
    return render_to_response(template,
                              {'participant_list': Registration.objects.all().order_by('last_name'),},)
