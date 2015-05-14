from django import template
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import mark_safe, escape
from django.utils import dateformat
from django.utils.formats import get_format
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse

register = template.Library()

@register.inclusion_tag('objlist/row.html', takes_context=True)
def show_row(context, obj):    
    data = {'fields': get_object_fields(context, obj, context['view'])}
    if context['view'].detail_url:
        data['detail_url'] = reverse(context['view'].detail_url, kwargs={context['view'].detail_url_kwarg: getattr(obj, context['view'].detail_url_kwarg)})
    return data

@register.simple_tag(takes_context=True)
def show_grid_cell(context, obj):    
    t = template.loader.get_template(context['view'].get_grid_template())
    return t.render(template.Context({'object': obj}))
    

def get_object_fields(context, obj, view):
    if not view.list_display:
        yield {'data': obj, 'style': ''}
          
    for field_name in view.list_display:
        try:
            f = obj._meta.get_field(field_name)
        except models.FieldDoesNotExist:
            # For non-field list_display values, the value is either a method
            # or a property.
            try:
                attr = getattr(obj, field_name)
                allow_tags = getattr(attr, 'allow_tags', False)
                if callable(attr):
                    attr = attr()
                if field_name in view.list_transforms:
                    result_repr = view.list_transforms[field_name](attr)
                else:
                    result_repr = smart_str(attr)
            except (AttributeError, ObjectDoesNotExist):
                result_repr = ''
            else:
                # Strip HTML tags in the resulting text, except if the
                # function has an "allow_tags" attribute set to True.
                if not allow_tags:
                    result_repr = escape(result_repr)
        else:
            field_val = getattr(obj, f.attname)
            if field_name in view.list_transforms:
                result_repr = mark_safe(view.list_transforms[field_name](field_val))
            elif isinstance(f.rel, models.ManyToOneRel):
                if field_val is not None:
                    try:
                        result_repr = escape(getattr(obj, f.name))
                    except (AttributeError, ObjectDoesNotExist):
                        result_repr = ''
                else:
                    result_repr = ''
                    
 
                
            # Dates and times are special: They're formatted in a certain way.
            elif isinstance(f, models.DateField) or isinstance(f, models.TimeField):
                if field_val:
                    (date_format, datetime_format, time_format) = get_format('DATE_FORMAT'), get_format('DATETIME_FORMAT'), get_format('TIME_FORMAT')
                    if isinstance(f, models.DateTimeField):
                        result_repr = dateformat.format(field_val, datetime_format).title()
                    elif isinstance(f, models.TimeField):
                        result_repr = dateformat.time_format(field_val, time_format).title()
                    else:
                        result_repr = dateformat.format(field_val, date_format).title()
                else:
                    result_repr = ''
            # Booleans are special: We use images.
            elif isinstance(f, models.BooleanField) or isinstance(f, models.NullBooleanField):
                result_repr = _boolean_icon(field_val)
            # DecimalFields are special: Zero-pad the decimals.
            elif isinstance(f, models.DecimalField):
                if field_val is not None:
                    result_repr = ('%%.%sf' % f.decimal_places) % field_val
                else:
                    result_repr = ''
            # Fields with choices are special: Use the representation
            # of the choice.
            elif f.choices:
                m_name = 'get_{0}_display'.format(field_name)
                result_repr = getattr(obj, m_name)()
            else:
                result_repr = escape(smart_str(field_val))
                
        yield {'data': result_repr, 'style': view.list_styles.get(field_name, '')}

def _boolean_icon(field_val):
    if field_val:
        return mark_safe('<i class="fa fa-check-circle"></i>')
    else:
        return '' 

