from django.db import models
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from fancy.utils.models import BaseModel, MetadataModel, get_sentinel_user
from fancy.utils import slugify
from mptt.models import MPTTModel
from taggit.managers import TaggableManager

class Post(MetadataModel,BaseModel):
    title = models.CharField(_('Title'),max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user))
    content = models.TextField(_('Post Content'),blank=True)
    date = models.DateTimeField(_('Publish Date'), default=datetime.now())
    enable_comments = models.BooleanField(default=True)
    categories = models.ManyToManyField('Category')
    redirect_to = models.CharField(_('Redirect to'),help_text=_("Redirect this url to another url instead of showing"),blank=True,null=True,max_length=100)
    
    PUB_STATUS = (
        (0, _('Draft')),
        (1, _('Published')),
    )
    status = models.IntegerField(_('Status'),choices=PUB_STATUS, default=0)
    
    tags = TaggableManager(blank=True)
    
    class Meta(BaseModel.Meta):
        ordering = ('-date',)
        get_latest_by = 'date'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
    
    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs) # Call the "real" save() method.

    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', (), {'slug' : self.slug } )
    
    def get_link(self):
        if self.redirect_to:
            return self.redirect_to

        return self.get_absolute_url()

    def get_previous(self):
        return self.get_previous_by_date(status__exact=1)
        
    def get_next(self):
        return self.get_next_by_date(status__exact=1)
        
    def get_content(self):
        return self.content
        
class Category(MPTTModel,BaseModel):
    name = models.CharField(_('Category Name'), max_length=50)
    slug = models.SlugField(_('Slug'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    parent = models.ForeignKey("self", related_name="children", null=True, blank=True)
    
    class Meta(BaseModel.Meta):
        ordering = ('name',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def __unicode__(self):
        return self.name
        
    @models.permalink
    def get_absolute_url(self):
        return ('category_index', (), {'slug' : self.slug } )
        
    def get_last_post(self):
        return Post.objects.filter(categories=self,status=1)[0]
    
    def post_count(self):
        return Post.objects.filter(categories=self,status=1).count()
    
    def last_post_date(self):
        return self.get_last_post().date
