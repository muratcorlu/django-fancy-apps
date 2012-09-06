# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from fancy.pages.models import Page
from fancy.utils.models import Attribute
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

import elementtree.ElementTree as ET
from datetime import datetime

class Command(BaseCommand):
    args = 'backup_file'
    help = 'Imports pages from another blog engines (Wordpress)'

    def handle(self, *args, **options):
        try:
            xml = ET.parse( args[0] )
        except:
            raise CommandError('First argument must be valid Wordpress backup file')
        
        """
        Namespaces
        
            xmlns:excerpt="http://wordpress.org/export/1.1/excerpt/"
        	xmlns:content="http://purl.org/rss/1.0/modules/content/"
        	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
        	xmlns:dc="http://purl.org/dc/elements/1.1/"
        	xmlns:wp="http://wordpress.org/export/1.1/"
        """
        
        wpns = "{http://wordpress.org/export/1.1/}"
        
        """
        import pages
        
        <item>
        		<title>Çorum Gazetesi</title>
        		<link>http://ahmetturanalkan.net/?page_id=2658</link>
        		<pubDate>Thu, 01 Jan 1970 00:00:00 +0000</pubDate>
        		<dc:creator>admin</dc:creator>
        		<guid isPermaLink="false">http://ahmetturanalkan.net//</guid>
        		<description></description>
        		<content:encoded><![CDATA[Page content]]></content:encoded>
        		<excerpt:encoded><![CDATA[]]></excerpt:encoded>
        		<wp:post_id>2658</wp:post_id>
        		<wp:post_date>2007-03-20 22:27:30</wp:post_date>
        		<wp:post_date_gmt>0000-00-00 00:00:00</wp:post_date_gmt>
        		<wp:comment_status>open</wp:comment_status>
        		<wp:ping_status>open</wp:ping_status>
        		<wp:post_name></wp:post_name>
        		<wp:status>draft</wp:status>
        		<wp:post_parent>2582</wp:post_parent>
        		<wp:menu_order>0</wp:menu_order>
        		<wp:post_type>page</wp:post_type>
        		<wp:post_password></wp:post_password>
        		<wp:is_sticky>0</wp:is_sticky>
        		<wp:postmeta>
        			<wp:meta_key>_wp_page_template</wp:meta_key>
        			<wp:meta_value><![CDATA[default]]></wp:meta_value>
        		</wp:postmeta>
        	</item>
       
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
        """
        Page.objects.all().delete()
        
        Wordpress_ID_conversions = {}
        parents = {}
        
        post_count = 0
        
        for post in xml.findall("channel/item"):
            if post.find("%spost_type" % wpns).text == 'page':
                author_name = post.find("{http://purl.org/dc/elements/1.1/}creator").text
                author, created = User.objects.get_or_create(username=author_name)

                newPost = Page(created_by=author, last_updated_by=author)

                title = post.find("title").text
                
                newPost.title = 'Untitled page'
                
                if title:
                    newPost.title = title
                else:
                    if newPost.status == 1:
                        self.stderr.write("No TITLE found for post '%s'.\n" % newPost.title )

                newPost.status = 1 if post.find("%sstatus" % wpns).text == 'publish' else 0
                newPost.slug = ''
                
                slug = post.find("%spost_name" % wpns).text
                
                if slug:
                    newPost.slug = slug
                else:
                    if newPost.status == 1:
                        self.stderr.write("No SLUG data found for post '%s'.\n" % newPost.title )
                
                newPost.content = ''
                
                content = post.find("{http://purl.org/rss/1.0/modules/content/}encoded").text
                
                if content:
                    newPost.content = content
                else:
                    if newPost.status == 1:
                        self.stderr.write("No CONTENT data found for post '%s'.\n" % newPost.title )
                
                newPost.show_in_menu = True
                newPost.order_number = int(post.find("%spost_parent" % wpns).text)
                try:
                    newPost.created_date = datetime.strptime( post.find("%spost_date" % wpns).text, "%Y-%m-%d %H:%M:%S")
                    newPost.last_modified = datetime.strptime( post.find("%spost_date" % wpns).text, "%Y-%m-%d %H:%M:%S")
                except:
                    pass
                
                # Save to get an id
                newPost.save()
                
                post_id = post.find("%spost_id" % wpns).text
                Wordpress_ID_conversions[post_id] = newPost.id
                
                parent_id = post.find("%spost_parent" % wpns).text
                
                if parent_id:
                    parents[post_id] = parent_id
                
                # meta data
                """ page_type = ContentType.objects.get_for_model(Page)
                
                for meta in post.findall("%spostmeta" % wpns):
                    
                    key = meta.find("%smeta_key" % wpns).text
                    if not key: continue
                    value = meta.find("%smeta_value" % wpns).text
                    if not value: value = ''
                    
                    pm = Attribute(content_type=page_type, object_id=newPost.id, key=key, value=value)
                    pm.save()
                    
                """
                
                post_count += 1
                
                self.stdout.write("Title: %s \n" % newPost.title )
        
        self.stdout.write("Writing parent-child relations... \n")
        
        for post_id, parent_id in parents.iteritems():
            if int(parent_id) > 0:
                real_post = Page.objects.get(pk=Wordpress_ID_conversions[post_id])
                real_post.parent = Page.objects.get(pk=Wordpress_ID_conversions[parent_id])
                real_post.save()
        
        self.stdout.write("Relations wrote.\n")
        
        self.stdout.write('%s pages succesfully imported.\n' % post_count)