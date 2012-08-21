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

admin.site.register(Album,AlbumAdmin)
