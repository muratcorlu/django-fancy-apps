from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class FancyPagesConfig(AppConfig):
    name = 'fancy.pages'
    verbose_name = _("Pages")
