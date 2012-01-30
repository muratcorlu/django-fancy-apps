from django.db import models
from datetime import datetime
#from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext_lazy as _
#from tinymce import models as tinymce_models
from fancy.utils.thumbs import ImageWithThumbsField
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel
from taggit.managers import TaggableManager

import uuid, os
def get_upload_path(instance, filename):
	ext = filename.split('.')[-1]
	original_filename = filename.replace('.'+ext, '')
	#filename = "%s.%s" % (uuid.uuid4(), ext)
	# Path: images/album_slug/image_slug/images_slug.ext
	image_slug = slugify(original_filename)
	if instance.slug:
		image_slug = instance.slug

	filename = "%s/%s/%s.%s" % ('posts',image_slug,image_slug,ext.lower())
	return os.path.join('images/', filename)

class Post(models.Model):
	title = models.CharField(_('Title'),max_length=200)
	slug = models.SlugField(_('Slug'), max_length=200)
	content = models.TextField(_('Post Content'),blank=True)
	date = models.DateTimeField(_('Publish Date'), default=datetime.now())
	enable_comments = models.BooleanField(default=True)
	categories = models.ManyToManyField('Category')
	featured_image = ImageWithThumbsField(_('Featured Image'), upload_to=get_upload_path, sizes=((80,80),(640,200),), fixed=True, blank=True)
	redirect_to = models.CharField(_('Redirect to'),help_text=_("Redirect this url to another url instead of showing"),blank=True,null=True,max_length=100)
	
	PUB_STATUS = (
		(0, _('Draft')),
		(1, _('Published')),
	)
	status = models.IntegerField(_('Status'),choices=PUB_STATUS, default=0)
	
	tags = TaggableManager(blank=True)
	
	class Meta:
		ordering = ('-date',)
		get_latest_by = 'date'
		verbose_name = _('Post')
		verbose_name_plural = _('Posts')
	
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
		
	def get_meta(self,key):
	    return self.meta_data.objects.get(key=key)
	
	def metadata(self):
	    dic = {}
	    for mt in self.meta_data.all():
	        dic[mt.key] = mt.value
	    
	    return dic

	def get_content(self):
		return self.content
		
class Category(MPTTModel):
	name = models.CharField(_('Category Name'), max_length=50)
	slug = models.SlugField(_('Slug'), max_length=200)
	description = models.TextField(_('Description'), blank=True)
	parent = models.ForeignKey("self", related_name="children", null=True, blank=True)
	
	class Meta:
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

class PostMeta(models.Model):
    post = models.ForeignKey('Post', related_name="meta_data")
    key = models.CharField(_('Key'), max_length=50 )
    value = models.CharField(_('Value'), max_length=500, blank=True)
    
    class Meta:
        ordering = ('post','key')
        verbose_name = _('Post Meta Data')
        verbose_name_plural = _('Post Meta Data')
    
    def __unicode__(self):
        return self.key
