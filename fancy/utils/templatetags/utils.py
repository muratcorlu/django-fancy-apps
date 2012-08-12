from django import template
register = template.Library()

@register.filter
def getKey(dict, key):
    return dict.get(key, '')