from django import forms
from django.forms.fields import DateField
from django.db.models import Q
from scheduler.models import *
from scheduler import widgets
from datetime import datetime, timedelta
from django.contrib.admin.widgets import AdminDateWidget

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
            Q(
                end_date__gte=data['start_date'],
                end_date__lte=data['end_date'],
                last_shift__gte=data['first_shift'],
                last_shift__lte=data['last_shift'],
            ) |
            Q(
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

        return data

class BasicForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    
    class Meta:
        fields = ('id',)

class AdminEditForm(VisitForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    beamline = forms.ModelChoiceField(queryset=Beamline.objects.all(), required=True)
    description = widgets.LargeCharField(required=True, help_text=Visit.HELP['description'])
    start_date = DateField(widget=widgets.LeftHalfDate, required=True)
    end_date = DateField(widget=widgets.RightHalfDate, required=True)
    first_shift = forms.ChoiceField(choices=Visit.SHIFT_CHOICES, widget=widgets.LeftHalfSelect, required=True)
    last_shift = forms.ChoiceField(choices=Visit.SHIFT_CHOICES, widget=widgets.RightHalfSelect, required=True)
    remote = widgets.LeftCheckBoxField(required=False, help_text=Visit.HELP['remote'])
    mail_in = widgets.RightCheckBoxField(required=False, help_text=Visit.HELP['mail_in'])
    purchased = widgets.LeftCheckBoxField(required=False, label="Purchased Access", help_text=Visit.HELP['purchased'])
    maintenance = widgets.RightCheckBoxField(required=False, label="Beamline Maintenance", help_text=Visit.HELP['maintenance'])
    
    class Meta:
        model = Visit
        fields = ('id','beamline','description', 'remote','mail_in','purchased','maintenance','start_date','end_date','first_shift','last_shift')

    def __init__(self, *args, **kwargs):
        super(VisitForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        '''Override clean to check for overlapping visits'''
        data = super(VisitForm, self).clean()
   
        for field in self.fields:
            try: 
                val = data[field]
            except:
                msg = 'Please enter a valid %s' % (field)
                self._errors[field] = self.error_class([msg])
                raise forms.ValidationError(msg)
   
        # Overlaps should apply to relevant beamline and not include self if editing
        blvisits = Visit.objects.filter(beamline__exact=data['beamline']).exclude(pk=data['id'])
        
        overlaps = blvisits.filter(
            Q(end_date__gt=data['start_date'],end_date__lt=data['end_date'],) 
            |
            Q(start_date__gt=data['start_date'],start_date__lt=data['end_date'],)  
            |
            Q(end_date__exact=data['end_date'],end_date__gt=data['start_date'],
              first_shift__lte=data['last_shift'],)
            |
            Q(end_date__exact=data['end_date'],start_date__lt=data['end_date'],
              last_shift__gte=data['first_shift'],)
            |
            Q(end_date__exact=data['end_date'],start_date__exact=data['start_date'],
              last_shift__gte=data['first_shift'],last_shift__lte=data['last_shift'],)
            |
            Q(start_date__exact=data['start_date'],start_date__lt=data['end_date'],
              first_shift__gte=data['first_shift'],)
            |
            Q(start_date__exact=data['start_date'],end_date__gt=data['start_date'],
              first_shift__lte=data['first_shift'],)
            |
            Q(start_date__exact=data['start_date'],end_date__exact=data['end_date'],
              first_shift__gte=data['first_shift'],first_shift__lte=data['last_shift'],)
        )
        
        if overlaps.count() > 0:
            conflicts = [v.description for v in overlaps.all()]
            msg = 'This visit overlaps with existing visits:\n %s!' % (', '.join(conflicts))
            self._errors['description'] = self.error_class([msg])
            raise forms.ValidationError(msg)

        if data['start_date'] > data['end_date'] or (data['start_date'] == data['end_date'] and data['first_shift'] > data['last_shift']):
            msg = 'Starting time cannot be after ending time!'
            self._errors['start_time'] = self.error_class([msg])
            raise forms.ValidationError(msg)
            
        blname = 'CMCF1'
        if blname is not 'CMCF1' and blname is not 'CMCF2':
            raise forms.ValidationError(
                'This visit does not have a selected beamline'
            )

        return data
        

class AdminOnCallForm(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput)
    local_contact = forms.ModelChoiceField(queryset=SupportPerson.objects.all(), required=True)
    
    class Meta:
        model = OnCall
        fields = ('date','local_contact')

class AdminVisitForm(forms.ModelForm):
    beamline = forms.ModelChoiceField(queryset=Beamline.objects.all(), required=True, widget=forms.HiddenInput)
    description = widgets.LargeCharField(required=True, help_text=Visit.HELP['description'])
    num_shifts = forms.IntegerField(widget=widgets.LeftHalfInput, initial=1, label='Number of Shifts' )
    first_shift = forms.IntegerField(required=True, widget=forms.HiddenInput)
    start_date = forms.DateField(widget=forms.HiddenInput)
    remote = widgets.LeftCheckBoxField(required=False, help_text=Visit.HELP['remote'])
    mail_in = widgets.RightCheckBoxField(required=False, help_text=Visit.HELP['mail_in'])
    purchased = widgets.LeftCheckBoxField(required=False, label="Purchased Access", help_text=Visit.HELP['purchased'])
    maintenance = widgets.RightCheckBoxField(required=False, label="Beamline Maintenance", help_text=Visit.HELP['maintenance'])
    
    
    class Meta:
        model = Visit
        fields = ('beamline','description', 'remote','mail_in','purchased','maintenance','num_shifts')
 
    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        try:
            parts = [cleaned_data.split('(')[0], cleaned_data.split('(')[1].split(')')[0]]
        except:
            msg = 'A name and proposal number are required. Please use the following format: Bruce Wayne (12-3456).'
            self._errors['description'] = self.error_class([msg])
            raise forms.ValidationError(msg)
        return cleaned_data
    
    def clean(self):
        '''Override clean to check for overlapping visits'''
        cleaned_data = self.cleaned_data
        data = super(AdminVisitForm, self).clean()
        # Overlaps should apply to relevant beamline and not include self if editing
        #obj = super(AdminVisitForm, self).save(commit=False)

        extra_shifts = ( data['num_shifts'] - ( 3 - data['first_shift'] ))
        extra_days = extra_shifts/3 + ( bool(extra_shifts%3) and 1 or 0 )
        end_date = datetime.strptime(str(data['start_date']), '%Y-%m-%d') + timedelta(days=extra_days)
        
        data['last_shift'] = ( data['first_shift'] + data['num_shifts'] - 1 ) % 3                  
        data['end_date'] = end_date.date()

        blvisits = Visit.objects.filter(beamline__exact=data['beamline'])
        
        overlaps = blvisits.filter(
            Q(end_date__gt=data['start_date'],end_date__lt=data['end_date'],) 
            |
            Q(start_date__gt=data['start_date'],start_date__lt=data['end_date'],)  
            |
            Q(end_date__exact=data['end_date'],end_date__gt=data['start_date'],
              first_shift__lte=data['last_shift'],)
            |
            Q(end_date__exact=data['end_date'],start_date__lt=data['end_date'],
              last_shift__gte=data['first_shift'],)
            |
            Q(end_date__exact=data['end_date'],start_date__exact=data['start_date'],
              last_shift__gte=data['first_shift'],last_shift__lte=data['last_shift'],)
            |
            Q(start_date__exact=data['start_date'],start_date__lt=data['end_date'],
              first_shift__gte=data['first_shift'],)
            |
            Q(start_date__exact=data['start_date'],end_date__gt=data['start_date'],
              first_shift__lte=data['first_shift'],)
            |
            Q(start_date__exact=data['start_date'],end_date__exact=data['end_date'],
              first_shift__gte=data['first_shift'],first_shift__lte=data['last_shift'],)
        )
        if overlaps.count() > 0:
            conflicts = [v.description for v in overlaps.all()]
            msg = 'This visit overlaps with existing visits:\n %s!' % (', '.join(conflicts))
            self._errors['description'] = self.error_class([msg])
            raise forms.ValidationError(msg)
        return data
    