from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
    
class RestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.file_types = kwargs.pop("file_types", ['application/pdf', 'image/jpeg', 'image/png', 'image/gif', 'text/plain'])
        self.max_size = kwargs.pop("max_size", 2621440)
        kwargs['help_text'] = u'Maximum size {0}, Formats: {1}.'.format(
                                            filesizeformat(self.max_size), 
                                            ','.join([t.split('/')[-1].upper() for t in self.file_types])
                                            )
        super(RestrictedFileField, self).__init__(*args, **kwargs)
        #print self.widget

    def clean(self, *args, **kwargs):        
        data = super(RestrictedFileField, self).clean(*args, **kwargs)        
        _file = data.file
        try:
            content_type = _file.content_type
            if content_type in self.file_types:
                if _file._size > self.max_size:
                    raise forms.ValidationError(_('{1} file exceeds maximum of {0}.').format(filesizeformat(self.max_size), filesizeformat(_file._size)))
            else:
                raise forms.ValidationError(_('File type not supported.'))
        except AttributeError:
            pass        
            
        return data
    
    def formfield(self, **kwargs):
        ff = super(RestrictedFileField, self).formfield(**kwargs)
        ff.widget.attrs.update(max_size=self.max_size, file_types=self.file_types)
        ff.max_size = self.max_size
        ff.file_types = {k:1 for k in self.file_types}
        return ff

from south.modelsinspector import add_introspection_rules
add_introspection_rules([
    (
        [RestrictedFileField], # Class(es) these apply to
        [],         # Positional arguments (not used)
        {           # Keyword argument
            "max_size": ["max_size", {"default": 2621440}],
            "file_types": ["file_types", {"default": ['application/pdf', 'image/jpeg', 'image/png']}],
        },
    ),
], ["^tasklist\.fields\.RestrictedFileField"])
