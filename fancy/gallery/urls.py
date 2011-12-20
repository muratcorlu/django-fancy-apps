from django.conf.urls.defaults import *


urlpatterns = patterns('fancy.gallery.views',
    url(r'^(?P<slug>[-\w\/]+)/$',
        view='album_detail',
        name='album_detail'
    ),
    url(r'^(?P<album_slug>[-\w\/]+)/(?P<album_item_slug>[-\w\/]+)$',
        view='album_item_detail',
        name='album_item_detail'
    ),
)
