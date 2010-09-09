from django import forms
from django.db import models
from scheduler.models import Visit, Beamline

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
    
    def clean(self):
        '''Override clean to check for overlapping visits'''
        data = super(VisitForm, self).clean()
   
        # Overlaps should apply to relevant beamline and not include self if editing
        obj = super(VisitForm, self).save(commit=False)

        blvisits = Visit.objects.filter(beamline__exact=data['beamline']).exclude(pk=obj.pk)
        
        overlaps = blvisits.filter(
            models.Q(
                end_date__gte=data['start_date'],
                end_date__lte=data['end_date'],
                last_shift__gte=data['first_shift'],
                last_shift__lte=data['last_shift'],
            ) |
            models.Q(
                start_date__gte=data['start_date'],
                start_date__lte=data['end_date'],
                first_shift__gte=data['first_shift'],
                first_shift__lte=data['last_shift'],
            )                 
        )
        
        if overlaps.count() > 0:
            conflicts = [v.description for v in overlaps.all()]
            raise forms.ValidationError(
                'This visit overlaps with existing visits:\n %s!' % (', '.join(conflicts))
            )
        #print models.ForeignKey(Beamline)
        blname = 'CMCF1'
        if blname is not 'CMCF1' and blname is not 'CMCF2':
            raise forms.ValidationError(
                'This visit does not have a selected beamline'
            )

#        if beamline = None:
#            raise forms.ValidationError(
#                'There is no Beamline selected for this visit'
#            )

        return data

