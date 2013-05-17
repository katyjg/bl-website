from django.db import models
from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class Application(models.Model):
    choices = ( ('yes','Yes'),
                ('no','No'),
              )
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=False)
    institution = models.CharField(max_length=100, )
    addr1 = models.CharField(_('Address'), max_length=100)
    addr2 = models.CharField(_(' '), max_length=100, blank=False)
    city = models.CharField(max_length=100)
    state = models.CharField(_('Province/State'), max_length=100)
    code = models.CharField(_('Area Code/ZipCode'), max_length=100)
    country = models.CharField(max_length=100)

    sup_name = models.CharField(_('supervisor Name'), max_length=100, blank=False)
    sup_email = models.EmailField(_('supervisor Email'), blank=False)
    sup_phone = models.CharField(_('supervisor Phone'), max_length=100, blank=False)

    undergrad = models.BooleanField(blank=False)
    masters = models.BooleanField(blank=False)
    phd = models.BooleanField(blank=False)
    postdoc = models.BooleanField(blank=False)
    faculty = models.BooleanField(blank=False)
    staff = models.BooleanField(blank=False)
    other = models.BooleanField(blank=False)
    other_text = models.CharField(_('Other'), max_length=100, blank=False)

    travel = models.BooleanField(_('Requests Travel Assistance'), blank=False)
    visa = models.BooleanField(_('Requires VISA'), blank=False)
    stay = models.BooleanField(_('Requests Accommodations'), blank=False)
    
    crystals = models.BooleanField(_('bringing crystals'))

    research = models.TextField(_('research Interests'))
    benefit = models.TextField(_('benefit/Experience'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    
    def __unicode__(self):
        return '%s, %s' % (self.name, self.institution)
    
    def year(self):
        return self.created.year
    
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'state', 'country','year')
admin.site.register(Application, ApplicationAdmin)


class Registration(models.Model):
    TALK_CHOICES = (
        (0, u'Poster'),
        (1, u'Oral'),
    )
    TITLE_CHOICES = (
        (0, u'Prof.'),
        (1, u'Dr.'),
        (2, u'Mr.'),
        (3, u'Ms.'),
        (4, u'Mrs.'),
        )
    # Personal Information
    title = models.IntegerField(choices=TITLE_CHOICES, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=False)
    institution = models.CharField(max_length=100, )
    addr1 = models.CharField(_('Address'), max_length=100)
    addr2 = models.CharField(_(' '), max_length=100, blank=False)
    city = models.CharField(max_length=100)
    state = models.CharField(_('Province/State'), max_length=100)
    code = models.CharField(_('Area Code/ZipCode'), max_length=100)
    country = models.CharField(max_length=100)

    undergrad = models.BooleanField(blank=False)
    masters = models.BooleanField(blank=False)
    phd = models.BooleanField(blank=False)
    postdoc = models.BooleanField(blank=False)
    faculty = models.BooleanField(blank=False)
    staff = models.BooleanField(blank=False)
    other = models.BooleanField(blank=False)
    other_text = models.CharField(_('Other'), max_length=100, blank=False)

    # Supervisor Information
    sup_name = models.CharField(_('supervisor Name'), max_length=100, blank=False)
    sup_email = models.EmailField(_('supervisor Email'), blank=False)
    sup_phone = models.CharField(_('supervisor Phone'), max_length=100, blank=False)

    # Abstract Submission
    talk = models.BooleanField()
    type = models.IntegerField(choices=TALK_CHOICES, blank=True, null=True)
    headline = models.CharField(_('Presentation Title'), max_length=500, blank=False)
    authors = models.CharField(_('Authors'), max_length=500, blank=False)
    abstract = models.TextField(_('Abstract'), blank=False)
    
    diet = models.TextField(_('Dietary Concerns'), blank=False)
    
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        unique_together = (("email"),)

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.institution)
    
    def name(self):
        return '%s %s %s' % (self.get_title_display(), self.first_name, self.last_name)
    
    def abstract_provided(self):
        return self.abstract and True or False
    
    
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'institution', 'state', 'country', 'talk','type','abstract_provided')
admin.site.register(Registration, RegistrationAdmin)