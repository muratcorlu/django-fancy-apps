from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def render_sub_pages(value):
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from beautifulsoup import BeautifulSoup
    
    content = BeautifulSoup(value, selfClosingTags=['sub_pages','img','br','input','meta','link','hr'])

    for inline in content.findAll('sub_pages'):
        try:
            template = inline["template"]
        except:
            template = "default.html"
        
        inline.replaceWith(render_to_string("fancy/pages/%s" %template, ))

    return mark_safe(content)

def render_inline_sub_pages(value):
    return "inlines(value)"