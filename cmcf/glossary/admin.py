from django.contrib import admin
from glossary.models import Term

class TermAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title']}
    list_display = ('title',)
    search_fields = ('title', 'description')
    class Media:
        js = ['/admin_media/tinymce/jscripts/tiny_mce/tiny_mce.js', '/admin_media/tinymce_setup/tinymce_setup.js',]

admin.site.register(Term, TermAdmin)
