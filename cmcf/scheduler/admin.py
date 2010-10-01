from django.contrib import admin

from scheduler.forms import VisitForm
from scheduler.models import Beamline, SupportPerson, Visit, OnCall, Stat, WebStatus

class VisitAdmin(admin.ModelAdmin):
    search_fields = ['description']
    form = VisitForm
    fieldsets = (
        (None, {
            'fields': ('beamline', 'description', ('start_date', 'first_shift'), ('end_date', 'last_shift')), 
        }),
    )
    
    

admin.site.register(Beamline)
admin.site.register(SupportPerson)
admin.site.register(Visit, VisitAdmin)
admin.site.register(OnCall)
admin.site.register(Stat)
admin.site.register(WebStatus)
