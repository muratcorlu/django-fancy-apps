from django.template.defaultfilters import slugify as slugify_original

def slugify(value):
    value = value.replace(u'\u0131', 'i')
    return slugify_original(value)
