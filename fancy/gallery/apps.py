from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class FancyGalleryConfig(AppConfig):
    name = 'fancy.gallery'
    verbose_name = _("Gallery")
