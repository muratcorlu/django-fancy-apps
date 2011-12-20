from django.db import models
from django import forms
from django.conf import settings
import settings as pages_settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from tinymce.widgets import TinyMCE
from tinymce import models as tinymce_models
from mptt.models import MPTTModel
from datetime import datetime

class Page(MPTTModel):
    language = models.CharField(_('Language'), max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    template = models.CharField(_('Page template'), max_length=50, choices=pages_settings.PAGE_TEMPLATES, default='default')
    order_number = models.PositiveSmallIntegerField(_('Order Number'),help_text=_('Page Order Number'),default=0)
    content = tinymce_models.HTMLField(_('Page Content'),blank=True)
    show_in_menu = models.BooleanField(_('Show in Menu'), default=False)
    redirect_to = models.CharField(_('Redirect to'),help_text=_("Redirect this url to another url instead of showing"),blank=True,null=True,max_length=100)
    created_date = models.DateTimeField(_('Publish Date'), default=datetime.now())
    last_modified = models.DateTimeField(_('Last Modified Date'), default=datetime.now())
    
    STATUSES = (
        ('0', _('Draft')),
        ('1', _('Active')),
    )
    status = models.CharField(_('Status'), max_length=1, choices=STATUSES, default='1')
    parent = models.ForeignKey('self', verbose_name=_(u'parent'), blank=True, null=True, related_name='children')
    
    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ('order_number', 'title')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.last_modified = datetime.now()
        if self.slug == '':
            self.slug = slugify(self.title)

        super(Page, self).save(*args, **kwargs) # Call the "real" save() method.
    
    def get_active_child_menus(self):
        return self.children.defer('content').filter(status=1,show_in_menu=True)
    
    def get_active_children(self):
        return self.children.filter(status=1).order_by('order_number','title')

    @models.permalink
    def get_absolute_url(self):
        if not getattr(self, '_slug', None):
            url = self.slug
            for ancestor in self.get_ancestors(True):
                url = ancestor.slug + u'/' + url
            self._slug = url    
        return ('pages_page_detail', (), {'slug' : str(self._slug) } )
    
