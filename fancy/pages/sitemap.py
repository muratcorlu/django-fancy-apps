from django.contrib.sitemaps import Sitemap
from models import Page

class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Page.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.last_modified


