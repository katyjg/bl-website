from django.contrib import admin
from blog.models import *

def highlight(modeladmin, request, queryset):
    queryset.update(highlight=True)
highlight.short_description = "Add to highlights"

def unhighlight(modeladmin, request, queryset):
    queryset.update(highlight=False)
unhighlight.short_description = "Remove from Highlights"

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status', 'highlight')
    list_filter   = ('publish', 'categories', 'status')
    actions = [highlight, unhighlight]
    search_fields = ('title', 'body')
    fieldsets = (
        (None, {
            'fields': ('title','slug','image','link','citation','body','tease','highlight','status','publish','categories'),
        }),
    )
    
    class Media:
        js = [getattr(settings, 'FEINCMS_RICHTEXT_INIT_CONTEXT', {}).get('TINYMCE_JS_URL',''), 
              '/static/grappelli/tinymce_setup/tinymce_setup.js',]    
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
