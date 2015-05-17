from django.core.exceptions import ValidationError
from crispy_forms.bootstrap import AppendedText, AccordionGroup, Accordion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Div, Field, HTML, BaseInput, Reset, ButtonHolder
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, FormActions
from django.core.urlresolvers import reverse_lazy
from django import forms
from datetime import datetime, timedelta
from django.utils.translation import ugettext as _
import models


class IssueForm(forms.ModelForm):
    class Meta:
        model = models.Issue
        fields = ('project', 'submitter', 'title','description','kind', 'priority', 'due_date', 'related')
        widgets = {'project': forms.HiddenInput, 'description': forms.Textarea(attrs={'rows': 5,}),
                   }
    
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "issue-form"
        self.helper.layout = Layout(
            Div(
                Div(Field('title', required=True),  css_class='col-sm-12'),
                Div(Field('description', required=True), css_class='col-sm-12'),
                Div(Field('kind', css_class="chosen"),  css_class='col-sm-6'),
                Div(Field('priority', css_class="chosen"), css_class='col-sm-6'),                                       
                Div(Field('due_date', css_class="datepicker"), css_class='col-sm-6'),
                Div(Field('related', css_class="chosen-value"), css_class='col-sm-6'),
                css_class="row narrow-gutter"
            ),                         
            Div(Div(
                   HTML('<hr/>'),
                   Div(StrictButton('Revert', type='reset', value='Reset', css_class="btn btn-default"),
                       StrictButton('Save', type='submit', value='Save', css_class='btn btn-primary'),
                       css_class='text-right col-xs-12'),                
                   css_class="row")),
            Field('project', type="hidden"),
            Field('submitter', type="hidden"),                        
        ) 

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = models.Issue
        fields = ('project', 'submitter', 'title','description', 'frequency', 'due_date', 'kind', 'priority')
        widgets = {'project': forms.HiddenInput, 'description': forms.Textarea(attrs={'rows': 5,}),
                   'kind': forms.HiddenInput, }
    def __init__(self, *args, **kwargs):
        super(MaintenanceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "issue-form"
        self.helper.layout = Layout(
            Div(
                Div(Field('title', required=True),  css_class='col-sm-12'),
                Div(Field('description', required=True), css_class='col-sm-12'),
                Div(Field('frequency', required=True),  css_class='col-sm-4'),
                Div(Field('priority', css_class="chosen"), css_class='col-sm-4'),                                       
                Div(Field('due_date', css_class="datepicker"), css_class='col-sm-4'),
                css_class="row narrow-gutter"
            ),                         
            Div(Div(
                   HTML('<hr/>'),
                   Div(StrictButton('Revert', type='reset', value='Reset', css_class="btn btn-default"),
                       StrictButton('Save', type='submit', value='Save', css_class='btn btn-primary'),
                       css_class='text-right col-xs-12'),                
                   css_class="row")),
            Field('project', type="hidden"),
            Field('submitter', type="hidden"),                        
        ) 
    
    def clean(self):
        data = super(MaintenanceForm, self).clean()
        data['kind'] = models.Issue.TYPES.maintenance
        data['status'] = models.Issue.STATES.pending
        if not data['due_date']:
            data['due_date'] = datetime.today() + timedelta(days=data['frequency']*30)
        return data
    
class CommentForm(forms.ModelForm):
    issue_kind = forms.ChoiceField(label="Type", required=False, choices=models.Issue.TYPES)
    issue_status = forms.ChoiceField(label="Status", required=False, choices=models.Issue.STATES)
    issue_priority = forms.ChoiceField(label="Priority", required=False, choices=models.Issue.PRIORITY)
    issue_owner = forms.ModelChoiceField(models.User.objects, label="Assign to", required=False)
    issue_due_date = forms.DateField(label="Due Date", required=False)
    issue_related = forms.ModelMultipleChoiceField(models.Issue.objects, label="Related to", required=False)
    class Meta:
        model = models.Comment
        fields = ('issue', 'author', 'description', 'kind')
        widgets = {'description': forms.Textarea(attrs={'rows': 3,}),}
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['issue_related'].queryset = models.Issue.objects.exclude(pk=self.initial['issue'].pk)
        self.helper = FormHelper()
        self.helper.form_class = "issue-form"
        if self.initial['issue'].kind == models.Issue.TYPES.maintenance:
            due_date_layout = Field('issue_due_date', css_class="datepicker", disabled=True)
            type_layout = Field('issue_kind', css_class="chosen", disabled=True)
        else:
            due_date_layout = Field('issue_due_date', css_class="datepicker")
            type_layout = Field('issue_kind', css_class="chosen")
        self.helper.layout = Layout(
            Div(
                Div(Field('description'), css_class='col-sm-12'),
                Div(Field('issue_owner', css_class="chosen"), css_class='col-sm-4'),                                       
                Div(type_layout,  css_class='col-sm-4'),
                Div(due_date_layout, css_class='col-sm-4'),
                Div(Field('issue_status', css_class="chosen"),  css_class='col-sm-4'),
                Div(Field('issue_priority', css_class="chosen"), css_class='col-sm-4'),                                       
                Div(Field('issue_related', css_class="chosen-value"), css_class='col-sm-4'),                                       
                css_class="row narrow-gutter"
            ),                         
            Div(Div(
                   HTML('<hr/>'),
                   Div(StrictButton('Revert', type='reset', value='Reset', css_class="btn btn-default"),
                       StrictButton('Save', type='submit', value='Save', css_class='btn btn-primary'),
                       css_class='text-right col-xs-12'),                
                   css_class="row")),
            Field('issue', type="hidden"),
            Field('author', type="hidden"),
            Field('kind', type="hidden"),                       
        )
    
    def clean(self):
        data = super(CommentForm, self).clean()
        issue = data['issue']
        descr = {
            'kind': 'Type',
            'owner': 'Assigned to',
            'due_date': 'Due',
            'status': 'Status',
            'priority': 'Priority',
            'related': 'Related Issues'
        }
        extra_txt = ''
        if issue.kind == models.Issue.TYPES.maintenance:
            del data['issue_kind']
            del data['issue_due_date']
            
        elif data['issue_kind'] == models.Issue.TYPES.maintenance:
            del data['issue_kind']
        
        # set comment kind to update if no comment text
        if not data['description']:
            data['kind'] = models.Comment.TYPES.update
        else:
            data['kind'] = models.Comment.TYPES.comment
            
        for k in ['kind', 'owner', 'due_date', 'status', 'priority', 'related']:
            ext_k = 'issue_{0}'.format(k)
            if not ext_k in data: continue
            cur_val = getattr(issue, k)
            new_val =  data[ext_k]
            if k == 'priority':
                cur_val = str(cur_val)
            elif k == 'related':
                cur_val = [o.pk for o in cur_val.all()]
                new_val = [o.pk for o in new_val]
            if cur_val != new_val and new_val:
                if k == 'priority':
                    val = models.Issue.PRIORITY[int(new_val)]
                if k == 'status':
                    val = models.Issue.STATES[new_val]
                elif k == 'related':
                    val = ", ".join(["<a href='{0}'>&nbsp;{1}&nbsp;</a>".format(reverse_lazy('issue-detail', kwargs={'pk':pk}),pk) for pk in new_val])
                else:
                    val = new_val
                extra_txt += u'<span class="label label-default">{0}: {1}</span>&nbsp;'.format(descr[k], val)
        if not data['description'] and not extra_txt:
            raise ValidationError('Nothing Changed')
        data['description'] = u"{0}<p>{1}</p>".format(data['description'] , extra_txt)
        return data

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = models.Attachment
        fields = ('user', 'issue', 'file')
        widgets = {'issue': forms.HiddenInput, 'user': forms.HiddenInput}

    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse_lazy('add-issue-attachment', kwargs={'pk': self.initial['issue'].pk})
        self.helper.layout = Layout(
            Div(Div(Field('file', template="tasklist/file_input.html"), css_class="col-xs-12"),
                css_class="row no-space"
                ),
                Field('issue', type="hidden"),
                Field('user', type="hidden"),
            )

