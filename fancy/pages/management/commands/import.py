# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from fancy.blog.models import Post, Category, PostMeta
import elementtree.ElementTree as ET

class Command(BaseCommand):
    args = 'backup_file'
    help = 'Imports posts from another blog engines (Wordpress)'

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
        
        """
        import categories
        
        <wp:category><wp:term_id>5</wp:term_id><wp:category_nicename>aksiyon</wp:category_nicename><wp:category_parent></wp:category_parent><wp:cat_name><![CDATA[Aksiyon Dergisi]]></wp:cat_name><wp:category_description><![CDATA[Aksiyon Dergisi'nde yayımlanan köşe yazıları]]></wp:category_description></wp:category>
        """
        
        category_count = 0
        
        for category in xml.findall("channel/{http://wordpress.org/export/1.1/}category"):
            category_count += 1
        
        self.stdout.write('%s categories succesfully imported.\n' % category_count)
        
        """
        import tags
        
        <wp:tag><wp:term_id>462</wp:term_id><wp:tag_slug>1-mayis</wp:tag_slug><wp:tag_name><![CDATA[1 Mayıs]]></wp:tag_name></wp:tag>
        """
        
        tag_count = 0
        
        for tag in xml.findall("channel/{http://wordpress.org/export/1.1/}tag"):
            tag_count += 1
        
        self.stdout.write('%s tags succesfully imported.\n' % tag_count)
        
        """
        import posts
        
        <item>
        		<title>Bir nevi hukuk akrobasisi</title> 
        		# <link>http://ahmetturanalkan.net/yazi/bir-nevi-hukuk-akrobasisi/</link>
        		<pubDate>Mon, 23 Jan 2012 01:40:38 +0000</pubDate>
        		# <dc:creator>admin</dc:creator>
        		# <guid isPermaLink="false">http://ahmetturanalkan.net/?p=5550</guid>
        		# <description></description>
        		<content:encoded><![CDATA[12 ….. etmektedir.]]></content:encoded>
        		# <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        		# <wp:post_id>5550</wp:post_id>
        		<wp:post_date>2012-01-23 04:40:38</wp:post_date>
        		<wp:post_date_gmt>2012-01-23 01:40:38</wp:post_date_gmt>
        		<wp:comment_status>open</wp:comment_status>
        		# <wp:ping_status>open</wp:ping_status>
        		<wp:post_name>bir-nevi-hukuk-akrobasisi</wp:post_name>
        		<wp:status>publish</wp:status>
        		# <wp:post_parent>0</wp:post_parent>
        		# <wp:menu_order>0</wp:menu_order>
        		# <wp:post_type>post</wp:post_type>
        		# <wp:post_password></wp:post_password>
        		# <wp:is_sticky>0</wp:is_sticky>
        		<category domain="category" nicename="aksiyon"><![CDATA[Aksiyon Dergisi]]></category>
        		<wp:postmeta>
        			<wp:meta_key>reference</wp:meta_key>
        			<wp:meta_value><![CDATA[http://www.aksiyon.com.tr/aksiyon/yazar-31661-bir-nevi--hukuk-akrobasisi.html]]></wp:meta_value>
        		</wp:postmeta>
        		<wp:postmeta>
        			<wp:meta_key>_edit_last</wp:meta_key>
        			<wp:meta_value><![CDATA[1]]></wp:meta_value>
        		</wp:postmeta>
        		<wp:postmeta>
        			<wp:meta_key>dsq_thread_id</wp:meta_key>
        			<wp:meta_value><![CDATA[554021788]]></wp:meta_value>
        		</wp:postmeta>
        	</item>
        """
        post_count = 0
        
        for item in xml.findall("channel/item"):
            if item.find("{http://wordpress.org/export/1.1/}post_type").text == 'post':
                post_count += 1
                #self.stdout.write("Title: %s \n" % item.find("title").text )
                    
        self.stdout.write('%s posts succesfully imported.\n' % post_count)