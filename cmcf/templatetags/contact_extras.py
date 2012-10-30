from django import template  
from scheduler.models import SupportPerson

register = template.Library()  
 
@register.filter("hide_email")  
def hide_email(value):  
	if len(value) <= max_length:  
         	return value  
   
     	truncd_val = value[:max_length]  
     	if value[max_length] != " ":  
         	rightmost_space = truncd_val.rfind(" ")  
        if rightmost_space != -1:  
             	truncd_val = truncd_val[:rightmost_space]  
   
     	return truncd_val + "..."   

@register.filter("email_part")
def email_part(value, position):
    return value.split('@')[position]

@register.filter("num_people")
def num_people(value):
    return len(SupportPerson.objects.filter(category=value))

