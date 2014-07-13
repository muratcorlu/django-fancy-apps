from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from models import Album, AlbumItem

def album_index(request):
    albums = Album.objects.filter(status=1).order_by('-date_created')
    return render(request, 'fancy/gallery/album_index.html', {'albums':albums})

def album_detail(request,slug):
    album = get_object_or_404(Album, slug=slug)
    return render(request, 'fancy/gallery/album_detail.html', {'album':album})
