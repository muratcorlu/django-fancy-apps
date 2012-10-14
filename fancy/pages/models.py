from django.db import models
from django import forms
from django.conf import settings
import settings as pages_settings
from django.utils.translation import ugettext_lazy as _
from fancy.utils import slugify
from fancy.utils.models import MetadataModel, BaseModel
from mptt.models import MPTTModel

class Page(MPTTModel,BaseModel,MetadataModel):
    language = models.CharField(_('Language'), max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, blank=True)
    template = models.CharField(_('Page template'), max_length=50, choices=pages_settings.PAGE_TEMPLATES, default='default')
    order_number = models.PositiveSmallIntegerField(_('Order Number'),help_text=_('Page Order Number'),default=0)
    content = models.TextField(_('Page Content'),blank=True)
    show_in_menu = models.BooleanField(_('Show in Menu'), default=False)
    redirect_to = models.CharField(_('Redirect to'),help_text=_("Redirect this url to another url instead of showing"),blank=True,null=True,max_length=100)
    
    STATUSES = (
        ('0', _('Draft')),
        ('1', _('Active')),
    )
    status = models.CharField(_('Status'), max_length=1, choices=STATUSES, default='1')
    parent = models.ForeignKey('self', verbose_name=_(u'parent'), blank=True, null=True, related_name='children')
    
    class Meta(BaseModel.Meta):
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    class MPTTMeta:
        order_insertion_by = ['order_number']

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)

        super(Page, self).save(*args, **kwargs) # Call the "real" save() method.

    def get_active_child_menus(self):
        return self.children.defer('content').filter(status=1,show_in_menu=True)
    
    def get_active_children(self):
        return self.children.filter(status=1).order_by('order_number','title')

    def render(self):
        if pages_settings.PAGE_DEFAULT_CONTENT_TYPE == 'md':
            from django.contrib.markup.templatetags.markup import markdown
            return markdown(self.content,'nl2br,markdown-urlize')

        return self.content

    @models.permalink
    def get_absolute_url(self):
        if not getattr(self, '_slug', None):
            url = self.slug
            for ancestor in self.get_ancestors(True):
                url = ancestor.slug + u'/' + url
            self._slug = url    
        return ('pages_page_detail', (), {'slug' : str(self._slug) } )
