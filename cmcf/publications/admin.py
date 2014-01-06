from django.contrib import admin

from publications.forms import PosterForm
from publications.models import *

class PublicationAdmin(admin.ModelAdmin):
    list_display  = ('get_authors', 'year', 'month','get_beamlines', 'get_title', 'journal')
    search_fields = ('title', 'year', 'authors', 'journal')
    fieldsets = (
        (None, {
            'fields': ('title','slug','authors','journal',('year','month','day'),'citation','original','pdb_entries','beamline'),
        }),
    )

#    class Media:
#        #js = ['/admin_media/tinymce/jscripts/tiny_mce/tiny_mce.js', '/admin_media/tinymce_setup/tinymce_setup.js',]
#        js = ['/admin_media/django-ckeditor/ckeditor/ckeditor.js']

class JournalAdmin(admin.ModelAdmin):
    list_display  = ('name', 'impact_factor','description')

class PosterAdmin(admin.ModelAdmin):
    list_display  = ('author','institution','title','presented')
    search_fields = ('title', 'author')
    form = PosterForm

#    class Media:
#        js = ['/admin_media/tinymce/jscripts/tiny_mce/tiny_mce.js', '/admin_media/tinymce_setup/tinymce_setup.js',]
    

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Poster, PosterAdmin)