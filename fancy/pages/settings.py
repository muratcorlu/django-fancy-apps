from django.conf import settings
from django.utils.translation import ugettext_lazy as _

PAGE_TEMPLATES = getattr(settings, 'PAGE_TEMPLATES', (
    ('default', _('Default')),
))

