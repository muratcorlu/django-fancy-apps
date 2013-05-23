from django.conf.urls.defaults import *
from sitemap import PageSitemap
from django.contrib.sitemaps.views import sitemap
sitemaps = {
    'pages': PageSitemap,
}

urlpatterns = patterns('',
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
    url(r'^(?P<slug>[-\w\/]+)/$',
        view='fancy.pages.views.page_detail',
        name='pages_page_detail'
    ),

)
