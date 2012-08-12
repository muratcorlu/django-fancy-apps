from django import template
from fancy.gallery.parser import inlines
import re

register = template.Library()

@register.filter
def render_gallery(value):
    return inlines(value)