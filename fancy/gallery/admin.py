from django.contrib import admin
from models import Album, Image
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail.shortcuts import get_thumbnail

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id','name','date_created')
    ordering = ('id',)

class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name','image','is_cover'),
        }),
        (_('Advanced Options'), {
            'classes':('collapse',),
            'fields':('description','order_number','slug')
        })
    )
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','_get_image_thumbnail')
    list_display_links = ('name','_get_image_thumbnail')
    search_fields = ['name']
    
    def _get_image_thumbnail(self,obj):
        mini = get_thumbnail(obj.image, '100x100', crop="center", upscale=False)
        return '<img src="%s" />' % mini.url
    _get_image_thumbnail.allow_tags = True
    _get_image_thumbnail.short_description = _('Image')
    

admin.site.register(Album,AlbumAdmin)
admin.site.register(Image,ImageAdmin)