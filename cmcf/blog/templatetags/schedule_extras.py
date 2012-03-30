from django import template  

register = template.Library()  
 
@register.filter("get_webmode")  
def get_webmode(value, index): 
    try:    
        return value[index]
    except:
        return ''   
