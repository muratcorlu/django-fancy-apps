from django.contrib import admin
from models import Page
from mptt.admin import MPTTModelAdmin
from django.utils.translation import ugettext_lazy as _
import admin_forms as forms

class PageAdmin(MPTTModelAdmin):
    form = forms.PageForm
    
    fieldsets = (
        (None, {
            'fields': ('title','content','parent'),
        }),
        (_('Advanced Options'), {
            'classes':('collapse',),
            'fields':('language','order_number','template','status','show_in_menu','redirect_to','slug')
        })
    )
    list_display = ('title','language','status','order_number')
    list_filter = ['language','status','level']
    list_editable = ('order_number',)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ['title']
    ordering = ('title',)


admin.site.register(Page,PageAdmin)