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
    sup_addr1 = models.CharField(_('supervisor Address'), max_length=100, blank=False)
    sup_addr2 = models.CharField(_(' '), max_length=100, blank=False)
    sup_city = models.CharField(_('supervisor City'), max_length=100, blank=False)
    sup_state = models.CharField(_('supervisor State/Province'), max_length=100, blank=False)
    sup_code = models.CharField(_('supervisor Area Code/Zip Code'), max_length=100, blank=False)
    sup_country = models.CharField(_('supervisor Country'), max_length=100, blank=False)

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
    crystals = models.BooleanField(_('bringing crystals'))

    research = models.TextField(_('research Interests'))
    benefit = models.TextField(_('benefit/Experience'))
    
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution',)
admin.site.register(Application, ApplicationAdmin)