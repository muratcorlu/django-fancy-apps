from django.shortcuts import redirect, get_list_or_404, render
from django.http import Http404
from models import Page

def page_detail(request, slug):

    parts = request.path_info.strip("/").split("/")

    pages = get_list_or_404(Page, slug=parts[-1])

    page = None

    if len(pages) > 1:
        print request.path_info
        for pg in pages:
            print pg.get_absolute_url()
            if pg.get_absolute_url() == request.path_info:
                page = pg

    if len(pages) == 1:
        page = pages[0]

    if not page:
        raise Http404

    if page.status == '0':
        if not request.user.is_authenticated():
            raise Http404

    if page.redirect_to:
        return redirect(page.redirect_to)

    template_file = 'fancy/pages/%s.html' % page.template

    return render(request, template_file, { 'page' : page })