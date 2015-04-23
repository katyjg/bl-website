from django import template  

register = template.Library()  
 
@register.filter("get_webmode")  
def get_webmode(value, index): 
    try:    
        return value[index]
    except:
        return ''   

@register.filter("find_in")
def find_in(string, value):
    return value in string