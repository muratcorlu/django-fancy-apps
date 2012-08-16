# coding=utf-8
from django.contrib import admin
from models import Category, Product, ProductMeta
#from fancy.gallery.models import Image
from django.utils.translation import ugettext_lazy as _

class MetaInline(admin.TabularInline):
    model = ProductMeta
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name','price','status']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (None, {
            'fields': ('category','name','description','images'),
        }),
        (_('Extra informations'), {
            'fields': ('price','status','slug','max_count')
        })
    )

    inlines = [MetaInline]

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)