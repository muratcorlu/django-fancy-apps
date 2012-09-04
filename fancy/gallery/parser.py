from django.template import TemplateSyntaxError
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.utils.encoding import smart_unicode
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from models import Album

def inlines(value, return_list=False):
    try:
        from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup
    except ImportError:
        from beautifulsoup import BeautifulStoneSoup, BeautifulSoup
    
    content = BeautifulSoup(value, selfClosingTags=['gallery','img','br','input','meta','link','hr'])
    inline_list = []

    if return_list:
        for inline in content.findAll('gallery'):
            rendered_inline = render_inline(inline)
            inline_list.append(rendered_inline['context'])
        return inline_list
    else:
        for inline in content.findAll('gallery'):
            rendered_inline = render_inline(inline)
            if rendered_inline:
                inline.replaceWith(render_to_string(rendered_inline['template'], rendered_inline['context']))
            else:
                inline.replaceWith('')
        return mark_safe(content)


def render_inline(inline):
    """
    Replace inline markup with template markup that matches the
    appropriate app and model.

    """

    # Look for inline type, 'app.model'
    try:
        id = inline['id']
    except:
        if settings.DEBUG:
            raise TemplateSyntaxError, "Couldn't find the attribute 'id' in the <gallery> tag."
        else:
            return ''

    album = Album.objects.get(pk=id)
    context = { 'album': album, }

    template = ["fancy/gallery/inline_album.html"]
    rendered_inline = {'template':template, 'context':context}

    return rendered_inline