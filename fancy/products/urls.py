from django.conf.urls.defaults import *

urlpatterns = patterns('fancy.products.views',
    url(r'^$', 'main', name="products_main" ),
    url(r'^(?P<slug>[\w\-\/]+)/$', 'main_controller', name="products_full_tree" ),
)
