from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
register = template.Library()

"""
Usage:

{% load mailform %} <!-- Loads mailform templatetag library -->

{% show_mailform %} <!-- Shows default.html form -->

{% show_mailform "contact_form.html" %} <!-- Shows contact_form.html form -->

"""
@register.simple_tag(takes_context=True)
def show_mailform(context, template="default.html"):
    return render_to_string("fancy/mailform/%s" % template, {}, context_instance=context )

"""
Usage:

page.content has mailform tag like that: <mailform template="contact_form.html" />

{{ page.content|render_mailform }}
"""
@register.filter
def render_mailform(value, context=None):
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        from beautifulsoup import BeautifulSoup

    content = BeautifulSoup(value, selfClosingTags=['mailform','img','br','input','meta','link','hr'])

    for inline in content.findAll('mailform'):
        try:
            tpl = inline["template"]
        except:
            tpl = "default.html"

        if context:
            rendered = render_to_string("fancy/mailform/%s" % tpl, {}, context_instance=context)
        else:
            rendered = render_to_string("fancy/mailform/%s" % tpl, {})

        inline.replaceWith(BeautifulSoup(rendered))

    return mark_safe(content)