from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from application_form.forms import ApplicationForm
from application_form.models import Application

def application_form(request, form_class=ApplicationForm,
                 template_name='application_form/application_form.html',
                 success_url=None, extra_context=None,
                 fail_silently=False):

    if success_url is None:
        success_url = reverse('application_form_sent')
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, request=request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        institution = request.POST.get('institution', '')
        addr1 = request.POST.get('addr1', '')
        addr2 = request.POST.get('addr2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        code = request.POST.get('code', '')
        country = request.POST.get('country', '') 
        sup_name = request.POST.get('sup_name', '')
        sup_email = request.POST.get('sup_email', '')
        sup_phone = request.POST.get('sup_phone', '')
        sup_addr1 = request.POST.get('sup_addr1', '')
        sup_addr2 = request.POST.get('sup_addr2', '')
        sup_city = request.POST.get('sup_city', '') 
        sup_state = request.POST.get('sup_state', '') 
        sup_code = request.POST.get('sup_code', '') 
        sup_country = request.POST.get('sup_country', '') 
        undergrad = request.POST.get('undergrad', '') 
        masters = request.POST.get('masters', '') 
        phd = request.POST.get('phd', '') 
        postdoc = request.POST.get('postdoc', '') 
        faculty = request.POST.get('faculty', '') 
        staff = request.POST.get('staff', '') 
        other = request.POST.get('other', '') 
        other_text = request.POST.get('other_text','')
	if request.POST.get == 'yes':
		travel = 1
	elif request.POST.get == 'no':
		travel=0
        #travel = request.POST.get('travel', '') 
        visa = request.POST.get('visa', '') 
        crystals = request.POST.get('crystals', '') 
        research = request.POST.get('research', '') 
        benefit = request.POST.get('benefit', '') 
        applicant = Application(name=name, email=email, phone=phone, institution=institution, addr1=addr1, addr2=addr2, city=city, state=state, code=code, country=country, sup_name=sup_name, sup_email=sup_email, sup_phone=sup_phone, sup_addr1=sup_addr1, sup_addr2=sup_addr2, sup_city=sup_city, sup_state=sup_state, sup_code=sup_code, sup_country=sup_country, undergrad=undergrad, masters=masters, phd=phd, postdoc=postdoc, faculty=faculty, staff=staff, other=other, other_text=other_text, travel=travel, visa=visa, crystals=crystals, research=research, benefit=benefit)

        applicant.save()
        if form.is_valid():
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
        else:
            retry_url = reverse('application_form_retry')
            return HttpResponseRedirect(retry_url)
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
    
def applicant_list(request):
    applicant_list = []
    for applicant in Application.objects.all():
        applicant_list.append(applicant)

    return render_to_response(
        'application_form/applicant_list.html', 
        {
            'applicant_list': applicant_list,
        },
        )
