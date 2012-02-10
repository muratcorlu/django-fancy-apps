from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Location(models.Model):
    name = models.CharField(_("Location Name"), max_length=150)
    lat = models.FloatField(_("Location Latitude"))
    lon = models.FloatField(_("Location Longitude"))
    created_date = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, verbose_name=_('Added by'),editable=False)
    
    def save(self, *args, **kwargs):
        self.added_by = self.request.user

        super(Location, self).save(*args, **kwargs) # Call the "real" save() method.
    
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

class Event(models.Model):
    name = models.CharField(_("Event Name"), max_length=250)
    date_start = models.DateTimeField(_("Event Start Date"),blank=True)
    date_end = models.DateTimeField(_("Event End Date"))
    location = models.ForeignKey(Location)
    description = models.TextField(_('Event Description'),blank=True)
    status = models.IntegerField(default=0,choices=EVENT_STATUSES)
    created_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, verbose_name=_('Owner'),editable=False)
    
    def save(self, *args, **kwargs):
        self.owner = self.request.user

        super(Event, self).save(*args, **kwargs) # Call the "real" save() method.
    
    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('-date_start',)

    def __unicode__(self):
        return self.name