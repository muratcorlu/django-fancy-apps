from fancy.events.models import Event, Location
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    fields = ('name','date_start','date_end','location','description','status')
    list_display = ('name', 'date_start')
    search_fields = ['name']
    date_hierarchy = 'date_start'

    def save_model(self, request, obj, form, change): 
        instance = form.save(commit=False)
        instance.owner = request.user
        instance.save()
        return instance

admin.site.register(Event, EventAdmin)

class LocationAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change): 
        instance = form.save(commit=False)
        instance.added_by = request.user
        instance.save()
        return instance

admin.site.register(Location, LocationAdmin)
