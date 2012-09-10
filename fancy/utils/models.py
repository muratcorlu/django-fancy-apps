from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver

"""
from mptt.managers import TreeManager
from mptt.models import MPTTModel

TODO: BaseModel with versionning support
class BaseManager(models.Manager):
    def get_query_set(self):
        return super(BaseManager, self).get_query_set().filter(deleted_flag=False)

    def all_with_deleted(self):
        return super(BaseManager, self).get_query_set(related_id=0)

class MPTTBaseManager(BaseManager, TreeManager):
    pass

"""
def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), editable=False, related_name="%(app_label)s_%(class)s_created")
    created_date = models.DateTimeField(_('Added date'), auto_now_add=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), editable=False, related_name="%(app_label)s_%(class)s_updated")
    last_updated_date = models.DateTimeField(_('Last update date'), auto_now=True)
    """
    related_id = models.IntegerField(default=0,editable=False)
    deleted_flag = models.BooleanField(_('Deleted'),default=False, editable=False)

    objects = BaseManager()
    
    def versions(self):
        #Returns old versions of current record
        return self.__class__.objects.filter(related_id=self.id, deleted_flag=False)

    def is_deleted(self):
        return self.deleted_flag

    def delete(self,permanent=False):
        if permanent:
            super(BaseModel,self).delete(self)
        else:
            self.deleted_flag = True
            self.save()
    """

    class Meta:
        abstract = True
        get_latest_by = "created_date"
        ordering = ("-created_date",)
        """
        FIXME: Permission must be model specific. Now it's App specific
        https://code.djangoproject.com/ticket/10686
        """
        permissions = (("can_view_deleted", _("Can view deleted rows")),)

"""
@receiver(pre_save)
def version(sender, instance, **kwargs):
    # check if model is an instance of BaseModel abstract model
    if isinstance(instance, BaseModel):
        # if the instance has no id, it is created
        current_id = instance.id
        if current_id:
            old = instance
            old.pk = None
            old.id = None
            old.related_id = current_id
            old.deleted_flag = True
            old.save()

class MPTTBaseModel(BaseModel, MPTTModel):
    _default_manager = MPTTBaseManager()

    class Meta:
        abstract = True
"""

class MetadataModel(models.Model):
    _metadata = None
    def metadata(self):
        if not self._metadata:
            self._metadata = {}
            metadata_type = ContentType.objects.get_for_model(self)
            for mt in Attribute.objects.filter(content_type__pk=metadata_type.id, object_id=self.id):
                self._metadata[mt.key] = mt.value
        
        return self._metadata

    def get_meta(self,key):
        metadata_type = ContentType.objects.get_for_model(self)
        return Attribute.objects.filter(content_type__pk=metadata_type.id, object_id=self.id, key=key)
    
    class Meta:
        abstract = True

class Attribute(BaseModel):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    key = models.CharField(_('Key'), max_length=50)
    value = models.TextField(_('Value'), blank=True)
    
    class Meta:
        ordering = ('content_type','key')
        verbose_name = _('Meta Data')
        verbose_name_plural = _('Meta Data')
    
    def __unicode__(self):
        return self.key

