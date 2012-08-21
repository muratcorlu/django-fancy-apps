from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fancy.utils.models import BaseModel

class Location(BaseModel):
    name = models.CharField(_("Location Name"), max_length=150)
    lat = models.FloatField(_("Location Latitude"))
    lon = models.FloatField(_("Location Longitude"))
    
    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

EVENT_STATUSES = (
	(0, _('Unpublished')),
	(1, _('Public')),
	(2, _('Private')),
)

class Event(BaseModel):
    name = models.CharField(_("Event Name"), max_length=250)
    date_start = models.DateTimeField(_("Event Start Date"))
    date_end = models.DateTimeField(_("Event End Date"))
    location = models.ForeignKey(Location,verbose_name=_('Location'))
    description = models.TextField(_('Event Description'),blank=True)
    status = models.IntegerField(_('Status'),default=0,choices=EVENT_STATUSES)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),editable=False)
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('-date_start',)

    def __unicode__(self):
        return self.name