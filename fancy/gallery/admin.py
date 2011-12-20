from django.contrib import admin
from models import Album, AlbumItem

from django.utils.translation import ugettext_lazy as _

class AlbumItemInline(admin.TabularInline):
    model = AlbumItem
    exclude = ['slug','date_added']

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    #inlines = [AlbumItemInline,]
    list_display = ('id','name','date_created')
    ordering = ('id',)

class AlbumItemAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
	list_display = ('image_img','name','album','description')
	list_filter = ['album']
	search_fields = ['name']

admin.site.register(Album,AlbumAdmin)
admin.site.register(AlbumItem,AlbumItemAdmin)