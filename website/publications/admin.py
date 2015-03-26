from django.contrib import admin
from django.conf import settings

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

    class Media:
        js = [getattr(settings, 'FEINCMS_RICHTEXT_INIT_CONTEXT', {}).get('TINYMCE_JS_URL',''), 
              '/admin_media/grappelli/tinymce_setup/tinymce_setup.js',]  

class JournalAdmin(admin.ModelAdmin):
    list_display  = ('name', 'impact_factor','description')

class PosterAdmin(admin.ModelAdmin):
    list_display  = ('author','institution','title','presented')
    search_fields = ('title', 'author')
    form = PosterForm

    class Media:
        js = [getattr(settings, 'FEINCMS_RICHTEXT_INIT_CONTEXT', {}).get('TINYMCE_JS_URL',''), 
              '/admin_media/grappelli/tinymce_setup/tinymce_setup.js',]  
    

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(Poster, PosterAdmin)