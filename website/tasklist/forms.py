
from crispy_forms.bootstrap import AppendedText, AccordionGroup, Accordion
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Button, Div, Field, HTML, BaseInput, Reset, ButtonHolder
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, FormActions
from django.core.urlresolvers import reverse_lazy
from django import forms
from django.utils.translation import ugettext as _
import models



class IssueForm(forms.ModelForm):
    class Meta:
        model = models.Issue
        fields = ('project', 'submitter', 'title','description','kind', 'priority', 'due_date')
        widgets = {'project': forms.HiddenInput, 'description': forms.Textarea(attrs={'rows': 5,}),}
    
    def __init__(self, *args, **kwargs):
        super(IssueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "issue-form"
        self.helper.layout = Layout(
            Div(
                Div(Field('title', required=True),  css_class='col-sm-12'),
                Div(Field('description', required=True), css_class='col-sm-12'),
                Div(Field('kind', css_class="chosen"),  css_class='col-sm-4'),
                Div(Field('priority', css_class="chosen"), css_class='col-sm-4'),                                       
                Div(Field('due_date', css_class="dateinput"), css_class='col-sm-4'),
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


class CommentForm(forms.ModelForm):
    issue_kind = forms.ChoiceField(label="Type", required=False, choices=models.Issue.TYPES)
    issue_status = forms.ChoiceField(label="Status", required=False, choices=models.Issue.STATES)
    issue_priority = forms.ChoiceField(label="Priority", required=False, choices=models.Issue.PRIORITY)
    issue_owner = forms.ModelChoiceField(models.User.objects, label="Assign to", required=False)
    issue_due_date = forms.CharField(label="Due Date", required=False)
    class Meta:
        model = models.Comment
        fields = ('issue', 'author', 'description')
        widgets = {'description': forms.Textarea(attrs={'rows': 3,}),}
    
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "issue-form"
        self.helper.layout = Layout(
            Div(
                Div(Field('description', required=True), css_class='col-sm-12'),
                Div(Field('issue_owner', css_class="chosen"), css_class='col-sm-4'),                                       
                Div(Field('issue_kind', css_class="chosen"),  css_class='col-sm-4'),
                Div(Field('issue_due_date', css_class="dateinput"), css_class='col-sm-4'),
                Div(Field('issue_status', css_class="chosen"),  css_class='col-sm-6'),
                Div(Field('issue_priority', css_class="chosen"), css_class='col-sm-6'),                                       
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
        )
    
    def clean(self):
        data = super(CommentForm, self).clean()
        issue = data['issue']
        descr = {
            'kind': 'Type',
            'owner': 'Assigned to',
            'due_date': 'Due',
            'status': 'Status',
            'priority': 'Priority'
        }
        extra_txt = ''
        for k in ['kind', 'owner', 'due_date', 'status', 'priority']:
            ext_k = 'issue_{0}'.format(k)
            if getattr(issue, k) != data[ext_k] and data[ext_k]:
                if k in ['owner', 'due_date']:
                    val = data[ext_k]
                elif k =='kind':
                    val = models.Issue.TYPES[data[ext_k]]
                elif k == 'status':
                    val = models.Issue.STATES[data[ext_k]]
                elif k == 'priority':
                    val = models.Issue.PRIORITY[int(data[ext_k])]
                extra_txt += u'<span class="label label-default">{0}: {1}</span>&nbsp;'.format(descr[k], val)
        data['description'] = u"{0}<p>{1}</p>".format(data['description'] , extra_txt)
        return data
