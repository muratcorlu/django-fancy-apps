from django.db import models
from settings import GALLERY_ORIGINAL_IMAGESIZE
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from fancy.utils import slugify
from fancy.utils.models import BaseModel
import os
from PIL import Image as PILImage
from helpers import get_upload_path
from taggit.managers import TaggableManager
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

ALBUM_STATUSES = (
    (0, _('Private')),
    (1, _('Public')),
)

class Image(BaseModel):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    name = models.CharField(_('Item name'), max_length=200, blank=True)
    image = models.ImageField(_('Image'), upload_to=get_upload_path)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    order_number = models.IntegerField(_('Order number'), default=0)
    is_cover = models.BooleanField(_('Cover photo'))

    #tags = TaggableManager(blank=True)
        
    class Meta(BaseModel.Meta):
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def save(self, *args, **kwargs):
        if self.image and not GALLERY_ORIGINAL_IMAGESIZE == 0:
            width, height = GALLERY_ORIGINAL_IMAGESIZE.split('x')
            super(Image, self).save(*args, **kwargs)

            filename = os.path.join( settings.MEDIA_ROOT, self.image.name )
            image = PILImage.open(filename)

            image.thumbnail((int(width), int(height)), PILImage.ANTIALIAS)
            image.save(filename)
        
        if not self.slug:
            self.slug = slugify(self.name)
        
        super(Image, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.image.url

    @models.permalink
    def get_absolute_link(self):
        return ('album_item_detail', (), {'album_slug':self.album.slug, 'album_item_slug' : self.slug } )

# If sorl-thumbnail app is installed, bind image delete signal to thumbnail deletions
if 'sorl.thumbnail' in settings.INSTALLED_APPS:
    from sorl.thumbnail import delete
    from django.db.models.signals import post_delete
    from django.dispatch import receiver

    @receiver(post_delete, sender=Image)
    def delete_image_files(sender, instance, **kwargs):
        # delete thumbnails
        delete(instance.image)

class ModelWithImage(models.Model):
    images = generic.GenericRelation(Image)

    def cover(self):
        try:
            cover_item = self.images.get(is_cover=True)
        except:
            cover_item = self.images.latest()
        
        return cover_item

    class Meta:
        abstract = True


class Album(BaseModel, ModelWithImage):
    name = models.CharField(_('Album Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    status = models.SmallIntegerField(_('Status'),choices=ALBUM_STATUSES)
    
    class Meta(BaseModel.Meta):
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')

    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
     return ('album_detail', (), {'slug' : self.slug })
