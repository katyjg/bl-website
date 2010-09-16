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
#    prepopulated_fields = {'slug': ('title',)}
    class Media:
        js = ['/admin_media/tinymce/jscripts/tiny_mce/tiny_mce.js', '/admin_media/tinymce_setup/tinymce_setup.js',]
admin.site.register(Post, PostAdmin)


class BlogRollAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'sort_order',)
    list_editable = ('sort_order',)
#admin.site.register(BlogRoll)
