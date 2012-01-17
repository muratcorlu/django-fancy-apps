from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

try:
	from BeautifulSoup import BeautifulSoup
except ImportError:
	from beautifulsoup import BeautifulSoup

register = template.Library()

@register.filter
def render_sub_pages(value):
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

@register.filter
def render_inlines(value):
	content = BeautifulSoup(value, selfClosingTags=['inline','img','br','input','meta','link','hr'])

	for inline in content.findAll('inline'):
		params = {}
		for attr, value in inline.attrs:
			params[attr] = value

		id = inline["id"]
		try:
			template = inline["template"]
		except:
			template = inline["id"]

		inline.replaceWith(render_to_string("fancy/pages/inline_%s.html" % template, params ))
	
	return mark_safe(content)


