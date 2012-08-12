from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Event

def home(request):
    all_events = Event.objects.filter(status=1).order_by('-date_start')
    return render_to_response("events/list.html",{'all_events':all_events},context_instance=RequestContext(request))
    
def event_detail(request,id):
    event = get_object_or_404(Event, id=id)
    all_events = Event.objects.filter(status=1).order_by('-date_start')
    return render_to_response("events/detail.html",{'event':event, 'all_events':all_events},context_instance=RequestContext(request))
