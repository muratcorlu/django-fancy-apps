from django.contrib import admin
from django.conf import settings
from models import Album, Image
from django.utils.translation import ugettext_lazy as _
from fancy.utils.admin import BaseAdmin
from django.contrib.contenttypes import generic

class ImageInline(generic.GenericTabularInline):
    model = Image
    extra = 1
    prepopulated_fields = {"slug": ("name",)}

class AlbumAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('id','name')
    ordering = ('id',)

    inlines = [ImageInline,]

class ImageAdmin(BaseAdmin):
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
        image_url = self.image.url

        if 'sorl' in settings.INSTALLED_APPS:
            from sorl.thumbnail.shortcuts import get_thumbnail

            mini = get_thumbnail(obj.image, '100x100', crop="center", upscale=False)
            image_url = mini.url

        return '<img src="%s" width="100" />' % image_url
    _get_image_thumbnail.allow_tags = True
    _get_image_thumbnail.short_description = _('Image')
    

admin.site.register(Album,AlbumAdmin)
#admin.site.register(Image,ImageAdmin)