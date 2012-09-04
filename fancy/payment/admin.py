# coding=utf-8
from django.contrib import admin
from models import Category, Product, Order, OrderItem, Currency, OrderHistory
from django.utils.translation import ugettext_lazy as _

class ProductAdmin(admin.ModelAdmin):
	list_display  = ['name','price','status']
	search_fields = ['name']
	
	fieldsets = (
        (None, {
            'fields': ('name','price','currency','max_count','status'),
        }),
        (_('Cargo informations'), {
            'classes':('collapse',),
            'fields':('height','width','depth','weight')
        })
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['name','price','quantity','total_price','currency']
    readonly_fields = ['name','quantity','price','total_price','currency']

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['status','order_date']
    list_display = ['name', 'id', 'order_date', 'total_price', 'status']
    inlines = [OrderItemInline]
    fields = ['status','name','order_date','order_hash','email','user_id','invoice_data','address_data','payment_data','total_price', 'currency']
    readonly_fields = ['name','order_date','order_hash','email','user_id','invoice_data','address_data','payment_data','total_price', 'currency']

    def save_model(self, request, obj, form, change): 
        if 'status' in form.changed_data:
            log = OrderHistory(order=obj)
            log.user = request.user
            log.action = u'Sipariş durumu değiştirildi: %s' % obj.get_status_display()
            log.save()

        super(OrderAdmin, self).save_model(request, obj, form, change)



admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(OrderItem)
admin.site.register(Currency)
admin.site.register(OrderHistory)