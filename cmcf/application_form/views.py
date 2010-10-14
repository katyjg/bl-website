"""
View which can render and send email from a contact form.

"""

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from application_form.forms import ApplicationForm


def application_form(request, form_class=ApplicationForm,
                 template_name='application_form/application_form.html',
                 success_url=None, extra_context=None,
                 fail_silently=False):

    #
    # We set up success_url here, rather than as the default value for
    # the argument. Trying to do it as the argument's default would
    # mean evaluating the call to reverse() at the time this module is
    # first imported, which introduces a circular dependency: to
    # perform the reverse lookup we need access to application_form/urls.py,
    # but application_form/urls.py in turn imports from this module.
    #
    
    if success_url is None:
        success_url = reverse('application_form_sent')
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES, request=request)
        if form.is_valid():
            form.save(fail_silently=fail_silently)
            return HttpResponseRedirect(success_url)
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
