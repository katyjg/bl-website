from django import template  

register = template.Library()  
 
@register.filter("get_total")  
def get_total(dict):
    total = 0
    for k, v in dict.items():
        total += v
    return total