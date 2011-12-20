from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class Attribute(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    key = models.CharField(_('Key'), max_length=50)
    value = models.CharField(_('Value'), max_length=500, blank=True)
    
    class Meta:
        ordering = ('content_type','key')
        verbose_name = _('Meta Data')
        verbose_name_plural = _('Meta Data')
    
    def __unicode__(self):
        return self.key
