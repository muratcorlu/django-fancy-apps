from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from fancy.events.models import Event

info_dict = {
    'queryset': Event.objects.all(),
    'template_object_name': 'events'
}

"""    (r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^(?P<object_id>\d+)/$', 'django.views.generic.list_detail.object_detail', info_dict),
    url(r'^(?P<object_id>\d+)/results/$', 'django.views.generic.list_detail.object_detail', dict(info_dict, template_name='polls/results.html'), 'poll_results'),
"""

urlpatterns = patterns('',
    (r'^$', ListView.as_view(
                queryset=Event.objects.all(),
                context_object_name='events_list',
                template_name='events_list.html')),
)
