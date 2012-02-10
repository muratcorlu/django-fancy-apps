"""
A form field that defines a character database field, rendered in the Django
admin interface as one of the following popular maps:

Google Maps
Yahoo Maps (Ajax)
Yahoo Maps (Flash)

You need to set two setting in your settings.py:

``MAP_API`` is one of the following: "google", "yahoo" or "yahooflash"
``MAP_API_KEY`` is the API key provided by Google or Yahoo

"""

from django.db.models.fields import CharField
from django import oldforms
from django import newforms as forms
from django.utils.text import capfirst
from django.utils.html import escape
from django.template import loader, Context
from django.conf import settings

class CoordinatesFormField(oldforms.TextField):
    """
    Defines a custom admin form field and renders as an interactive map if
    Javascript is available. Otherwise a normal input text field is shown.
    """
    def render(self, data):
        if data is None:
            data = ''
        maxlength = ''
        if self.maxlength:
            maxlength = 'maxlength="%s" ' % self.maxlength
        if isinstance(data, unicode):
            data = data.encode(settings.DEFAULT_CHARSET)
        map_api = settings.MAP_API or None
        if map_api in ("google", "yahoo", "yahooflash"):
            template = loader.get_template("coordinates_form.html")
            context = Context({
              'field_name': self.field_name,
              'input_type': self.input_type,
              'map_id': self.get_id(),
              'class_name': self.__class__.__name__,
              'is_required': self.is_required and ' required' or '',
              'data': escape(data),
              'length': self.length,
              'maxlength': maxlength,
              'api': map_api,
              'api_key': settings.MAP_API_KEY or ""
            })
            return template.render(context)

class CoordinatesField(CharField):
    """
    Defines the form field which wraps around the custom CoordinatesFormField.
    Should also get a Widget for the future "oldforms-removal" era.
    """
    def __init__(self, *args, **kwargs):
        kwargs['maxlength'] = 70
        CharField.__init__(self, *args, **kwargs)

    def get_manipulator_field_objs(self):
        return [CoordinatesFormField]

    def formfield(self, **kwargs):
        defaults = {'required': not self.blank, 'label': capfirst(self.verbose_name), 'help_text': self.help_text}
        defaults.update(kwargs)
        return forms.CharField(**defaults)

    def get_internal_type(self):
        return 'CharField'