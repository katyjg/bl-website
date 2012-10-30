from django import template  
register = template.Library()  
 
@register.filter("gallery_title")  
def gallery_title(value):
	if value == 1:
		return "CMCF1 Images"
	elif value == 2:
		return "CMCF2 Images"
	elif value == 0:
		return "All Images"  

