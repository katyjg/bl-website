from django.contrib import admin

from scheduler.forms import VisitForm
from scheduler.models import Beamline, SupportPerson, Visit, OnCall, Stat, WebStatus

class VisitAdmin(admin.ModelAdmin):
    search_fields = ['description']
    list_display = ('beamline', 'description', 'start_date', 'first_shift', 'end_date', 'last_shift')
    form = VisitForm
    fieldsets = (
        (None, {
            'fields': ('beamline', 'description', ('start_date', 'first_shift'), ('end_date', 'last_shift')), 
        }),
    )

class OnCallAdmin(admin.ModelAdmin):
    search_fields = ['local_contact', 'date']
    list_display = ('date','local_contact')

class SupportPersonAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','phone_number','category','office')

admin.site.register(Beamline)
admin.site.register(SupportPerson, SupportPersonAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(OnCall, OnCallAdmin)
admin.site.register(Stat)
