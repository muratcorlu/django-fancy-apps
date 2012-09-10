from django.contrib import admin
from django.contrib.contenttypes import generic
from models import Attribute, BaseModel
from django.utils.translation import ugettext_lazy as _

class MetaInline(generic.GenericTabularInline):
    model = Attribute
    extra = 0

class BaseAdmin(admin.ModelAdmin):
    """
    def get_readonly_fields(self, request, obj=None):
        fs = super(BaseAdmin, self).get_readonly_fields(request, obj)
        fs += ('created_by', 'last_updated_by',)
        return fs

    def get_fieldsets(self, request, obj=None):
        fs = super(BaseAdmin, self).get_fieldsets(request, obj)
        
        fs[0][1]['fields'].remove('created_by')
        fs[0][1]['fields'].remove('last_updated_by')

        fs.extend([(_('Other informations'), {'fields':['created_by','last_updated_by'], 'classes':['collapse']})])
        return fs

    def changelist_view(self, request, extra_context=None):
        if request.user.has_perm('%s.can_view_deleted' % self.model._meta.app_label):
            if not "deleted_flag" in self.list_filter:
                self.list_filter += ("deleted_flag",)
        return super(BaseAdmin, self).changelist_view(request, extra_context)
    def queryset(self, request):
        return super(BaseAdmin, self).queryset(request).exclude(deleted_flag=True)
    """
    
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
