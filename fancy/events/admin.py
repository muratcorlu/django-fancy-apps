from fancy.events.models import Event, Location
from django.contrib import admin

class EventAdmin(admin.ModelAdmin):
    #fieldsets = [
    #    (None, {'fields':['question']}),
    #    ('Date information', {'fields':['pub_date'], 'classes':['collapse']}),
    #]
    list_display = ('name', 'date_start')
    search_fields = ['name']
    date_hierarchy = 'date_start'

admin.site.register(Event, EventAdmin)
admin.site.register(Location)
