from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from models import Event

def home(request):
    all_events = Event.objects.filter(status=1).order_by('-date_start')
    return render(request, "events/list.html",{'all_events':all_events})

def event_detail(request,id):
    event = get_object_or_404(Event, id=id)
    all_events = Event.objects.filter(status=1).order_by('-date_start')
    return render(request, "events/detail.html",{'event':event, 'all_events':all_events})
