""" Newforms Admin configuration for Photologue

"""
from django.contrib import admin
from models import *

try:
    from batchadmin.admin import BatchModelAdmin
except ImportError:
    BatchModelAdmin = admin.ModelAdmin

class GalleryAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title',)}
    filter_horizontal = ('photos',)

def add_to_cmcf1(modeladmin, request, queryset):
    queryset.update(gallery='1')
add_to_cmcf1.short_description = "Move to CMCF1 Gallery"

def add_to_cmcf2(modeladmin, request, queryset):
    queryset.update(gallery='2')
add_to_cmcf2.short_description = "Move to CMCF2 Gallery"

def highlight(modeladmin, request, queryset):
    queryset.update(photo_highlight=True)
highlight.short_description = "Add to highlights"

def unhighlight(modeladmin, request, queryset):
    queryset.update(photo_highlight=False)
unhighlight.short_description = "Remove from Highlights"

class PhotoAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    actions = [add_to_cmcf1, add_to_cmcf2, highlight, unhighlight]
    list_display = ('title', 'gallery', 'date_taken', 'date_added', 'is_public', 'photo_highlight', 'tags', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title',)}

    class Media:
        js = ['/media/admin/tinymce/jscripts/tiny_mce/tiny_mce.js', '/media/admin/tinymce_setup/tinymce_setup.js',]

class PhotoEffectAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    list_display = ('name', 'description', 'color', 'brightness', 'contrast', 'sharpness', 'filters', 'admin_sample')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Adjustments', {
            'fields': ('color', 'brightness', 'contrast', 'sharpness')
        }),
        ('Filters', {
            'fields': ('filters',)
        }),
        ('Reflection', {
            'fields': ('reflection_size', 'reflection_strength', 'background_color')
        }),
        ('Transpose', {
            'fields': ('transpose_method',)
        }),
    )

class PhotoSizeAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    list_display = ('name', 'width', 'height', 'crop', 'pre_cache', 'effect', 'increment_count')
    fieldsets = (
        (None, {
            'fields': ('name', 'width', 'height', 'quality')
        }),
        ('Options', {
            'fields': ('upscale', 'crop', 'pre_cache', 'increment_count'), 'classes': ['collapse']
        }),
        ('Enhancements', {
            'fields': ('effect', 'watermark',), 'classes': ['collapse']
        }),
    )

class WatermarkAdmin(BatchModelAdmin):
    batch_actions = ['delete_selected']
    list_display = ('name', 'opacity', 'style')


#admin.site.register(Gallery, GalleryAdmin)
#admin.site.register(GalleryUpload)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoEffect, PhotoEffectAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
#admin.site.register(Watermark, WatermarkAdmin)
