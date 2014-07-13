from django.conf.urls import patterns, url

urlpatterns = patterns('fancy.products.views',
    url(r'^$', 'main', name="products_main" ),
    url(r'^(?P<slug>[\w\-\/]+)/$', 'main_controller', name="products_full_tree" ),
)
