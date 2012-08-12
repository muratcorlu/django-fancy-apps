from django.conf import settings
from django.utils.translation import ugettext_lazy as _

FORM_FROM = getattr(settings, 'FORM_FROM', "noreply@example.com")
FORM_RECIPIENTS = getattr(settings, 'FORM_RECIPIENTS', settings.MANAGERS)
FORM_SUBJECT = getattr(settings, 'FORM_SUBJECT', "Message from site")
