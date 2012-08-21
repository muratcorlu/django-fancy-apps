# coding=utf-8
from django.contrib import admin
from models import Category, Product
#from fancy.gallery.models import Image
from django.utils.translation import ugettext_lazy as _
from django.db import models
from fancy.utils.admin import MetaInline, BaseAdmin
from fancy.gallery.admin import ImageInline
from django.contrib.contenttypes import generic

class ProductAdmin(BaseAdmin):
    list_display  = ['name','price','status']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (None, {
            'fields': ('category','name','description',),
        }),
        (_('Extra informations'), {
            'classes':('collapse',),
            'fields': ('price','status','slug')
        })
    )
    inlines = [ImageInline,MetaInline]

class CategoryAdmin(BaseAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)