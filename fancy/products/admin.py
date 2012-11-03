# coding=utf-8
from django.contrib import admin
from models import Category, Product
#from fancy.gallery.models import Image
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.admin import MPTTModelAdmin
from fancy.utils.admin import MetaInline, BaseAdmin
from fancy.gallery.admin import ImageInline
from django.contrib.contenttypes import generic
from admin_forms import CategoryForm, ProductForm

class ProductAdmin(BaseAdmin):
    form = ProductForm
    
    list_display  = ['name','category','price','status','order_number']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ['category','status']
    list_editable = ('order_number',)
    ordering = ('order_number', 'id')

    fieldsets = (
        (None, {
            'fields': ['category','name','description',],
        }),
        (_('Extra informations'), {
            'classes':('collapse',),
            'fields': ('price','status','slug','order_number')
        })
    )
    inlines = [ImageInline,MetaInline]

class CategoryAdmin(MPTTModelAdmin,BaseAdmin):
    form = CategoryForm
    list_display = ['name','product_count']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ImageInline]

    def product_count(self, cat):
        return cat.products.count()
    product_count.admin_field = _('Product count')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)