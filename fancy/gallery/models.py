from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from fancy.utils.thumbs import ImageWithThumbsField
from datetime import datetime

class Album(models.Model):
    #language = models.CharField(_('Language'), max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    name = models.CharField(_('Album Name'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    date_created = models.DateTimeField(_('Creation Date'), default=datetime.now())
    #parent = models.ForeignKey('self', verbose_name=_(u'parent'), blank=True, null=True, related_name='children')
    
    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Album')
        ordering = ('-date_created',)

    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
     return ('album_detail', (), {'slug' : self.slug })

import uuid, os
def get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    original_filename = filename.replace('.'+ext, '')
    #filename = "%s.%s" % (uuid.uuid4(), ext)
    # Path: images/album_slug/image_slug/images_slug.ext
    image_slug = slugify(original_filename)
    if instance.slug:
        image_slug = instance.slug
    
    filename = "%s/%s/%s.%s" % (instance.album.slug,image_slug,image_slug,ext.lower())
    return os.path.join('images/', filename)

class AlbumItem(models.Model):
    album = models.ForeignKey(Album, related_name="items")
    name = models.CharField(_('Item name'), max_length=200, blank=True)
    image = ImageWithThumbsField(_('Image'), upload_to=get_upload_path, sizes=((80,80),(120,120),(800,600),), fixed=True)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    date_added = models.DateTimeField(_('Added date'), default=datetime.now())

    def image_img(self):
        if self.image:
            return u'<img src="%s" />' % self.image.url_80x80
        else:
            return '[]'
    
    image_img.short_description = 'Thumb'
    image_img.allow_tags = True
        
    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ("-date_added",)
    
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_link(self):
        return ('album_item_detail', (), {'slug' : self.slug } )
