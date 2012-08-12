import django.forms as forms
from string import Template
from django.utils.safestring import mark_safe
from django.conf import settings
import os

class ImageUploaderWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        tpl = Template(u'<img src="$url" />')
        print(attrs)
        url = "%s/%s" % (settings.MEDIA_URL, value)
        return mark_safe(tpl.substitute(url=url))