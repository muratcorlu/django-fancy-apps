from django.contrib import admin
from django.contrib.contenttypes import generic
from models import Attribute, BaseModel

class MetaInline(generic.GenericTabularInline):
    model = Attribute
    extra = 0

class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        obj.last_updated_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, BaseModel): #Check if it is the correct type of inline
                if not instance.created_by_id:
                    instance.created_by = request.user
                
                instance.last_updated_by = request.user            
                instance.save()
