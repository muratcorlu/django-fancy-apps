from django.conf.urls.defaults import *

urlpatterns = patterns('fancy.products.views',
    url(r'^$', 'main', name="products_main" ),
    url(r'^(?P<category_slug>[\w\-]+)/$', 'category_main', name="products_category_main" ),
    url(r'^(?P<category_slug>[\w\-]+)/(?P<product_slug>[\w\-]+)/$', 'detail', name="products_detail" ),
)
