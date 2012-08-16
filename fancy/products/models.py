from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
import settings
from fancy.gallery.models import Image
from datetime import datetime

class Category(MPTTModel):
    name = models.CharField(_('Product Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)
    
    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_('Product Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    price = models.DecimalField(_('Price'),max_digits=6,decimal_places=2,default=0)
    description = models.TextField(_('Description'))
    created_date = models.DateTimeField(_('Publish Date'), default=datetime.now())
    last_modified = models.DateTimeField(_('Last Modified Date'), default=datetime.now())
    max_count = models.IntegerField(_('Max order count'), default=1)
    
    category = models.ForeignKey(Category, related_name="products")

    STATUSES = (
        ('0', _('Out of stock')),
        ('1', _('In stock')),
    )
    status = models.CharField(_('Status'), max_length=1, choices=STATUSES, default='1')

    images = models.ManyToManyField(Image)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.last_modified = datetime.now()
        if self.slug == '':
            self.slug = slugify(self.name)

        super(Product, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def can_order_multiple(self):
        return self.max_count > 1
        
    def get_price_as_cent(self):
        return int(self.price * 100)

    _metadata = None
    def metadata(self):
        if not self._metadata:
            self._metadata = {}
            for mt in self.meta_data.all():
                self._metadata[mt.key] = mt.value
        
        return self._metadata

    @models.permalink
    def get_absolute_url(self):
        return ('payment_product_detail', (), {'slug' : str(self.slug) } )

class ProductMeta(models.Model):
    product = models.ForeignKey(Product, related_name="meta_data")
    key = models.CharField(_('Key'), max_length=50, choices=settings.PRODUCTS_META_CHOICES )
    value = models.TextField(_('Value'), blank=True)
    
    class Meta:
        ordering = ('product','key')
        verbose_name = _('Product Meta Data')
        verbose_name_plural = _('Product Meta Data')
    
    def __unicode__(self):
        return self.key
