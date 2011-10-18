from django.conf.urls.defaults import *


urlpatterns = patterns('fancy.pages.views',
    url(r'^(?P<slug>[-\w\/]+)/$',
        view='page_detail',
        name='pages_page_detail'
    ),
)
