from django.conf.urls import patterns, url
from feeds import LatestEntriesFeed
import settings
from sitemap import BlogSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'posts': BlogSitemap,
}

urlpatterns = patterns('fancy.blog.views',
    url(r'^$', 'index', name='post_index'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^rss/$', LatestEntriesFeed()),
	url(r'^(?P<year>[\d]{4})/$','year_index', name='post_year_index'),
	url(r'^(?P<year>[\d]{4})/(?P<month>[\d]{2})/$','month_index', name='post_month_index'),
	url(r'^(?P<slug>[-\w]+)/$', 'detail', name='post_detail'),
    url(r'^%s/(?P<slug>[-\w]+)/$' % settings.BLOG_CATEGORY_PATH, 'category_index', name='category_index'),
    url(r'^%s/(?P<slug>[-\w]+)/$' % settings.BLOG_TAG_PATH, 'tag_index', name='tag_index'),
)
