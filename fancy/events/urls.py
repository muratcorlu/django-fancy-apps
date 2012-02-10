from django.conf.urls.defaults import *

urlpatterns = patterns('fancy.events.views',
    # events/12/:
    url(r'^$', 'home', name='events_home'),
    url(r'^(?P<id>[\d]+)/$', 'event_detail', name='event_detail'),
)
