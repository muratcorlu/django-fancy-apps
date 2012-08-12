from models import Page

def pages_menu(request):
    return {'pages_menu': Page.objects.defer('content').filter(parent=None,show_in_menu=True,status=1).order_by('order_number')}
