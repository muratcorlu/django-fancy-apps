from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

def get_sentinel_user():
    return User.objects.get_or_create(username='deleted')[0]

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), editable=False, related_name="%(app_label)s_%(class)s_created")
    created_date = models.DateTimeField(_('Added date'), auto_now_add=True)
    last_updated_by = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), editable=False, related_name="%(app_label)s_%(class)s_updated")
    last_updated_date = models.DateTimeField(_('Last update date'), auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "created_date"
        ordering = ("-created_date",)

class MetadataModel(models.Model):
    _metadata = None
    def metadata(self):
        if not self._metadata:
            self._metadata = {}
            metadata_type = ContentType.objects.get_for_model(self)
            for mt in Attribute.objects.filter(content_type__pk=metadata_type.id, object_id=self.id):
                self._metadata[mt.key] = mt.value
        
        return self._metadata

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

