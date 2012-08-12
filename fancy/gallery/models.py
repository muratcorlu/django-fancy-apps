from django.db import models
from settings import GALLERY_ORIGINAL_IMAGESIZE, GALLERY_ENCRYPT_FILENAMES, GALLERY_DIR
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from fancy.utils import slugify
from datetime import datetime
from sorl.thumbnail.shortcuts import get_thumbnail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import hashlib
from django.core.files.base import File
import os
from django.conf import settings
from sorl.thumbnail import delete
from PIL import Image as PILImage

ALBUM_STATUSES = (
    (0, _('Private')),
    (1, _('Public')),
)


import uuid, os
def get_upload_path(instance, filename):
    parts = filename.split('.')
    ext = parts[-1]
    parts.pop()
    basename = '.'.join(parts)

    today = datetime.now()
    
    if GALLERY_ENCRYPT_FILENAMES:
        time_string = today.strftime("%H-%M-%S")
        hash = hashlib.sha224( "%s-%s" % (filename, time_string) ).hexdigest()
        path = os.path.join(GALLERY_DIR, "%s/%s/%s.%s" % (hash[:2], hash[2:4], hash, ext.lower()) )
    else:
        date_path = today.strftime("%Y/%m")
        
        path = os.path.join(GALLERY_DIR, date_path, "%s.%s" % (slugify(basename), ext.lower()))
        
    return path

class Image(models.Model):
    name = models.CharField(_('Item name'), max_length=200, blank=True)
    image = models.ImageField(_('Image'), upload_to=get_upload_path)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    date_added = models.DateTimeField(_('Added date'), auto_now_add=True)
    order_number = models.IntegerField(_('Order number'), default=0)
    is_cover = models.BooleanField(_('Cover photo'))
    
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ("-date_added",)
        get_latest_by = "date_added"
    
    def save(self, *args, **kwargs):
        if self.image and not GALLERY_ORIGINAL_IMAGESIZE == 0:
            width, height = GALLERY_ORIGINAL_IMAGESIZE.split('x')
            super(Image, self).save()

            filename = os.path.join( settings.SITE_ROOT, self.image.url.strip('/') )
            image = PILImage.open(filename)

            image.thumbnail((int(width), int(height)), PILImage.ANTIALIAS)
            image.save(filename)
        
        if not self.slug:
            self.slug = slugify(self.name)
        
        super(Image, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_link(self):
        return ('album_item_detail', (), {'album_slug':self.album.slug, 'album_item_slug' : self.slug } )


@receiver(post_delete, sender=Image)
def delete_image_files(sender, instance, **kwargs):
    # delete thumbnails
    delete(instance.image)

class Album(models.Model):
    name = models.CharField(_('Album Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    date_created = models.DateTimeField(_('Creation Date'), auto_now=True)
    last_modified = models.DateTimeField(_('Last Update Date'), auto_now=True)
    created_by = models.ForeignKey(User, verbose_name=_('Created by'))
    status = models.SmallIntegerField(_('Status'),choices=ALBUM_STATUSES)
    images = models.ManyToManyField(Image)
    
    def cover(self):
        try:
            cover_item = self.images.get(is_cover=True)
        except:
            cover_item = self.images.latest()
        
        return cover_item

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        ordering = ('-date_created',)
        get_latest_by = "date_created"

    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
     return ('album_detail', (), {'slug' : self.slug })
