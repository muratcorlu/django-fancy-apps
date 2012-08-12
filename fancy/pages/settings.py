from django.conf import settings
from django.utils.translation import ugettext_lazy as _

PAGE_TEMPLATES = getattr(settings, 'PAGE_TEMPLATES', (
    ('default', _('Default')),
))
PAGE_VERSIONING = getattr(settings, 'PAGE_VERSIONING', True)
PAGE_DEFAULT_CONTENT_TYPE = getattr(settings, 'PAGE_DEFAULT_CONTENT_TYPE', 'md')
PAGE_CONTENT_EDITORS = getattr(settings, 'PAGE_CONTENT_EDITORS', {
    'text':'textfield',
    'html':'tinymce',
    'md':'pagedown',
})
PAGE_META_CHOICES = getattr(settings, 'PAGE_META_CHOICES', None)