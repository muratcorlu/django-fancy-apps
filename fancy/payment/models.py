from django.db import models
from django.conf import settings
#import settings as payment_settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel
from datetime import datetime
from fancy.utils.fields import JSONField
from django.contrib.auth.models import User
import hashlib

class Category(models.Model):
    name = models.CharField(_('Product Category Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    description = models.TextField(_('Description'), blank=True)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)
    
    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name

class Currency(models.Model):
    prefix = models.CharField(_('Currency prefix'),blank=True, max_length=10)
    postfix = models.CharField(_('Currency postfix'),blank=True, max_length=10)
    name = models.CharField(_('Currency name'), max_length=20)
    exchange_rate = models.DecimalField(_('Exchange rate'), default=1, max_digits=11, decimal_places=10)
    
    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(_('Product Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    price = models.DecimalField(_('Price'),max_digits=6,decimal_places=2)
    currency = models.ForeignKey(Currency)
    created_date = models.DateTimeField(_('Publish Date'), auto_now_add=True)
    last_modified = models.DateTimeField(_('Last Modified Date'), auto_now=True)
    max_count = models.IntegerField(_('Max order count'), default=1, help_text=_('Maximum number of items you can sell for one order.'))
    
    height = models.IntegerField(_('Product packet height (cm)'), default=0)
    width = models.IntegerField(_('Product packet width (cm)'), default=0)
    depth = models.IntegerField(_('Product packet depth (cm)'), default=0)
    weight = models.IntegerField(_('Product packet weight (gr)'), default=0)
    
    STATUSES = (
        ('0', _('Out of stock')),
        ('1', _('In stock')),
    )
    status = models.CharField(_('Status'), max_length=1, choices=STATUSES, default='1')
    
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

    @models.permalink
    def get_absolute_url(self):
        return ('payment_product_detail', (), {'slug' : str(self.slug) } )

class Order(models.Model):
    order_hash = models.CharField(_('Order Unique Hash'),max_length=128,blank=True)
    name = models.CharField(_('Buyer name'), max_length=50)
    email = models.EmailField(_('Buyer email'))
    user_id = models.IntegerField(_('Buyer User ID'),default=0)
    invoice_data = JSONField(_('Invoice Data'))
    address_data = JSONField(_('Recipient Address'))
    payment_data = JSONField(_('Payment Data'))

    STATUSES = (
        (0, _('Pending')),
        (10, _('Pending Payment Approval')),
        (20, _('Processing')),
        (30, _('Shipped')),
        (40, _('Complete')),
        (50, _('Canceled')),
    )
    status = models.IntegerField(_('Order Status'),choices=STATUSES)
    order_date = models.DateTimeField(_('Order Date'), auto_now_add=True)
    total_price = models.DecimalField(_('Order Total Price'),max_digits=6,decimal_places=2)
    currency = models.CharField(_('Currency'), max_length=20)
    currency_id = models.IntegerField(_('Currency ID'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ('-order_date',)
    
    def __unicode__(self):
        return u"%s" % self.order_hash

    def save(self, *args, **kwargs):
        self.order_hash = hashlib.sha224( "%s-%s-%s" % (self.id, self.order_date, self.total_price) ).hexdigest()
        super(Order, self).save(*args, **kwargs) # Call the "real" save() method.

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product_id = models.IntegerField(_('Product Id'))
    name = models.CharField(_('Product Name'), max_length=200)
    quantity = models.IntegerField(_('Product Quantity'))
    price = models.DecimalField(_('Unit Price'),max_digits=6,decimal_places=2)
    total_price = models.DecimalField(_('Total Price'),max_digits=6,decimal_places=2)
    currency = models.CharField(_('Currency'), max_length=20)
    currency_id = models.IntegerField(_('Currency ID'))

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
    
class OrderHistory(models.Model):
    order = models.ForeignKey(Order, related_name='logs')
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    action = models.CharField(_('Action'), max_length=200)

    def __unicode__(self):
        return "%s: %s" % (self.user, self.action)

    class Meta:
        verbose_name = _('Order History')
        verbose_name_plural = _('Order Histories')
        ordering = ('-date',)

