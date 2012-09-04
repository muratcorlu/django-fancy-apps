# coding: utf-8

from django.core.management.base import BaseCommand, CommandError
from fancy.blog.models import Post, Category
from fancy.utils.models import Attribute
from django.contrib.auth.models import User
import elementtree.ElementTree as ET
from datetime import datetime

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
        
        wpns = "{http://wordpress.org/export/1.1/}"
        
        """
        import categories
        
        <wp:category><wp:term_id>5</wp:term_id><wp:category_nicename>category-slug</wp:category_nicename><wp:category_parent></wp:category_parent><wp:cat_name><![CDATA[Category Name]]></wp:cat_name><wp:category_description><![CDATA[Category Description]]></wp:category_description></wp:category>
        """

        category_count = 0
        
        for category in xml.findall("channel/%scategory" % wpns):
            cat_slug = category.find("%scategory_nicename" % wpns).text
            
            # check is already exist
            if Category.objects.filter(slug=cat_slug).exists():
                continue

            cat_name = category.find("%scat_name" % wpns).text

            try:
                cat_desc = category.find("%scategory_description" % wpns).text
            except:
                cat_desc = ''
            
            cat_parent = category.find("%scategory_parent" % wpns).text

            # get or create imported user for category owner
            import_user, created = User.objects.get_or_create(username='imported')
        
            newCat = Category(name=cat_name, slug=cat_slug, description=cat_desc, created_by=import_user, last_updated_by=import_user)

            if cat_parent:
                try:
                    newCat.parent = Category.objects.get(slug=cat_parent)
                except:
                    pass
            
            newCat.save()
            
            self.stdout.write("Category named '%s' added.\n" % cat_name)
            
            category_count += 1
        
        self.stdout.write('%s categories succesfully imported.\n' % category_count)
        
        """
        import posts
        
        <item>
        		<title>Post title</title> 
        		# <link>http://example.com/2012/12/12/post-title/</link>
        		<pubDate>Mon, 12 Dec 2012 01:40:38 +0000</pubDate>
        		<dc:creator>admin</dc:creator>
        		# <guid isPermaLink="false">http://example.com/?p=5550</guid>
        		# <description></description>
        		<content:encoded><![CDATA[ Post Content ]]></content:encoded>
        		# <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        		# <wp:post_id>5550</wp:post_id>
        		<wp:post_date>2012-12-12 04:40:38</wp:post_date>
        		<wp:post_date_gmt>2012-12-12 01:40:38</wp:post_date_gmt>
        		<wp:comment_status>open</wp:comment_status>
        		# <wp:ping_status>open</wp:ping_status>
        		<wp:post_name>post-title</wp:post_name>
        		<wp:status>publish</wp:status>
        		# <wp:post_parent>0</wp:post_parent>
        		# <wp:menu_order>0</wp:menu_order>
        		# <wp:post_type>post</wp:post_type>
        		# <wp:post_password></wp:post_password>
        		# <wp:is_sticky>0</wp:is_sticky>
        		<category domain="category" nicename="category-slug"><![CDATA[Category Name]]></category>
        		<category domain="post_tag" nicename="tag-slug"><![CDATA[Tag Name]]></category>
        		<wp:postmeta>
        			<wp:meta_key>key</wp:meta_key>
        			<wp:meta_value><![CDATA[Valye]]></wp:meta_value>
        		</wp:postmeta>
        	</item>
        """
        Post.objects.all().delete()
        
        post_count = 0
        
        for post in xml.findall("channel/item"):
            if post.find("%spost_type" % wpns).text == 'post':
                author_name = post.find("{http://purl.org/dc/elements/1.1/}creator").text
                author, created = User.objects.get_or_create(username=author_name)

                newPost = Post(author=author, created_by=author, last_updated_by=author)

                title = post.find("title").text
                
                newPost.title = 'Untitled post'
                
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
                
                newPost.enable_comments = True if post.find("%scomment_status" % wpns).text == 'open' else False
                newPost.date = datetime.strptime( post.find("%spost_date" % wpns).text, "%Y-%m-%d %H:%M:%S")
                
                # Save to get an id
                newPost.save()
                
                for taxonomy in post.findall("category"):
                    # categories
                    if taxonomy.get("domain") == 'category':
                        postCat = Category.objects.get(slug=taxonomy.get("nicename"))
                        newPost.categories.add(postCat)
                    
                    #tags
                    if taxonomy.get("domain") == 'post_tag':
                        newPost.tags.add( taxonomy.text )
                
                newPost.save()

                # meta data
                for meta in post.findall("%spostmeta" % wpns):
                    key = meta.find("%smeta_key" % wpns).text
                    if not key: continue
                    value = meta.find("%smeta_value" % wpns).text
                    if not value: value = ''
                    
                    pm = Attribute(content_object=newPost, key=key, value=value, created_by=newPost.author, last_updated_by=newPost.author)
                    pm.save()
                    
                
                post_count += 1
                
                self.stdout.write("Title: %s \n" % newPost.title )
                    
        self.stdout.write('%s posts succesfully imported.\n' % post_count)