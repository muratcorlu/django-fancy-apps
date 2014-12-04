from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class FancyBlogConfig(AppConfig):
    name = 'fancy.blog'
    verbose_name = _("Blog")
