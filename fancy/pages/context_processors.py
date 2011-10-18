from models import Page

def pages_menu(request):
    return {'pages_menu': Page.objects.filter(parent=None,show_in_menu=True,status=1)}
