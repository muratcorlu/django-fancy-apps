from fancy.events.models import Event, Location
from django.contrib import admin
from fancy.utils.admin import BaseAdmin

class EventAdmin(BaseAdmin):
    fields = ('name','date_start','date_end','location','description','status')
    list_display = ('name', 'owner', 'date_start')
    search_fields = ['name']
    date_hierarchy = 'date_start'

    def save_model(self, request, obj, form, change): 
        instance = form.save(commit=False)
        instance.owner = request.user
        instance.save()
        return instance

admin.site.register(Event, EventAdmin)
admin.site.register(Location, BaseAdmin)
