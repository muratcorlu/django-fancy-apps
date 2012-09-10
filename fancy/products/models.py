from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
import settings
from fancy.gallery.models import Image, ModelWithImage
from datetime import datetime
from fancy.utils.models import MetadataModel, BaseModel
from django.contrib.contenttypes import generic

class Category(MPTTModel, BaseModel, ModelWithImage):
    name = models.CharField(_('Category name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = _('Product category')
        verbose_name_plural = _('Product categories')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        if not getattr(self, '_slug', None):
            slugs = [ancestor.slug for ancestor in self.get_ancestors()]
            slugs.append(self.slug)
            
            url = '/'.join(slugs)

            self._slug = url    
        return ('products_full_tree', (), {'slug' : str(self._slug) } )


class Product(MetadataModel, ModelWithImage, BaseModel):
    name = models.CharField(_('Product name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    price = models.DecimalField(_('Price'),max_digits=6,decimal_places=2,default=0)
    description = models.TextField(_('Description'))
    
    category = models.ForeignKey(Category, verbose_name=_('Product category'), related_name="products")

    STATUSES = (
        ('0', _('Out of stock')),
        ('1', _('In stock')),
    )
    status = models.CharField(_('Status'), max_length=1, choices=STATUSES, default='1')
    
    class Meta(BaseModel.Meta):
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.name)

        super(Product, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def can_order_multiple(self):
        return self.max_count > 1
        
    def get_price_as_cent(self):
        return int(self.price * 100)

    @models.permalink
    def get_absolute_url(self):
        if not getattr(self, '_slug', None):
            slugs = [ancestor.slug for ancestor in self.category.get_ancestors()]
            slugs.append(self.category.slug)
            slugs.append(self.slug)
            
            url = '/'.join(slugs)

            self._slug = url    
        return ('products_full_tree', (), {'slug' : str(self._slug) } )
