from django import forms
from django.conf import settings
from django.core.mail import send_mail
#from django.core.mail import mail_admins
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import Site


# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary.
attrs_dict = { 'class': 'required' }

class ApplicationForm(forms.Form):
    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        super(ApplicationForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request
    
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)), label=u'Email (optional)', required=True)
    phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    institution = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=True)
    addr1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    addr2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    code = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)

    sup_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=True)
    sup_email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)), label=u'Email (optional)', required=True)
    sup_phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    sup_addr1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    sup_addr2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    sup_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    sup_state = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    sup_code = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)
    sup_country = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=u'Name (optional)', required=False)

    undergrad = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False)
    masters = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False)
    phd = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False)
    postdoc = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False)
    faculty = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False)
    staff = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False)
    other = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict), required=False)
    other_text = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), required=False)

    travel = forms.ChoiceField(widget=forms.RadioSelect(), choices[['Yes','Yes'],['No','No']] )
    visa = forms.ChoiceField(widget=forms.RadioSelect(), choices[['Yes','Yes'],['No','No']] )

    research = forms.CharField(widget=forms.Textarea(attrs=attrs_dict))
    benefit = forms.CharField(widget=forms.Textarea(attrs=attrs_dict))
    
    from_email = settings.DEFAULT_FROM_EMAIL
    
    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]

    subject_template_name = "application_form/application_form_subject.txt"
    
    template_name = 'application_form/application_form.txt'

    def message(self):
        """
        Render the body of the message to a string.
        
        """
        if callable(self.template_name):
            template_name = self.template_name()
        else:
            template_name = self.template_name
        return loader.render_to_string(template_name,
                                       self.get_context())
    
    def subject(self):
        """
        Render the subject of the message to a string.
        
        """
        subject = loader.render_to_string(self.subject_template_name,
                                          self.get_context())
        return ''.join(subject.splitlines())
    
    def get_context(self):
        """
        Return the context used to render the templates for the email
        subject and body.

        By default, this context includes:

        * All of the validated values in the form, as variables of the
          same names as their fields.

        * The current ``Site`` object, as the variable ``site``.

        * Any additional variables added by context processors (this
          will be a ``RequestContext``).
        
        """
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        return RequestContext(self.request,
                              dict(self.cleaned_data,
                                   site=Site.objects.get_current()))
    
    def get_message_dict(self):
        """
        Generate the various parts of the message and return them in a
        dictionary, suitable for passing directly as keyword arguments
        to ``django.core.mail.send_mail()``.

        By default, the following values are returned:

        * ``from_email``

        * ``message``

        * ``recipient_list``

        * ``subject``
        
        """
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")
        message_dict = {}
        for message_part in ('from_email', 'message', 'recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = callable(attr) and attr() or attr
        return message_dict
    
    def save(self, fail_silently=False):
        """
        Build and send the email message.
        
        """
        print self.get_message_dict()
        send_mail(fail_silently=fail_silently, **self.get_message_dict())
        
class AkismetContactForm(ApplicationForm):
    """
    Contact form which doesn't add any extra fields, but does add an
    Akismet spam check to the validation routine.

    Requires the setting ``AKISMET_API_KEY``, which should be a valid
    Akismet API key.
    
    """
    def clean_body(self):
        """
        Perform Akismet validation of the message.
        
        """
        if 'body' in self.cleaned_data and getattr(settings, 'AKISMET_API_KEY', ''):
            from akismet import Akismet
            from django.utils.encoding import smart_str
            akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                                  blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                 'referer': self.request.META.get('HTTP_REFERER', ''),
                                 'user_ip': self.request.META.get('REMOTE_ADDR', ''),
                                 'user_agent': self.request.META.get('HTTP_USER_AGENT', '') }
                if akismet_api.comment_check(smart_str(self.cleaned_data['body']), data=akismet_data, build_data=True):
                    raise forms.ValidationError(u"Akismet thinks this message is spam")
        return self.cleaned_data['body']
