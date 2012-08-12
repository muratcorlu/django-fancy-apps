from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import Album, AlbumItem

def album_index(request):
    albums = Album.objects.filter(status=1).order_by('-date_created')
    return render_to_response('fancy/gallery/album_index.html',{'albums':albums},context_instance=RequestContext(request))

def album_detail(request,slug):
    album = get_object_or_404(Album, slug=slug)
    return render_to_response('fancy/gallery/album_detail.html',{'album':album},context_instance=RequestContext(request))
