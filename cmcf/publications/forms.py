import os
import subprocess

from django import forms

from publications.models import Poster

class PosterForm(forms.ModelForm):
    class Meta:
        model = Poster

    def clean(self):
        '''Override clean to check for overlapping visits'''
        data = super(PosterForm, self).clean()
        
        msg = ''
        if data['file'].size > 10485760:
            msg = 'The file is too big.  Get it down to 10Mb and try uploading it again.'
        elif not data['file'].content_type == 'text/plain' or not len(data['file'].name.split('.')) == 2 or data['file'].name.split('.')[1] != 'pdf':
            msg = 'Check the format of your file.  Only .pdf files are allowed.'
                  
        if msg:
            raise forms.ValidationError(msg)
        return data
    
