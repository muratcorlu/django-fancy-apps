from django.conf import settings
from django.utils.translation import ugettext_lazy as _

PAYMENT_MAIL_FROM = getattr(settings, 'PAYMENT_MAIL_FROM', '')
PAYMENT_MAIL_RECIPIENTS = getattr(settings, 'PAYMENT_MAIL_RECIPIENTS', '')
PAYMENT_GATEWAY = getattr(settings, 'PAYMENT_GATEWAY', '')
PAYMENT_GATEWAY_SETTINGS = getattr(settings, 'PAYMENT_GATEWAY_SETTINGS', {
	merchant_id:'',
	merchant_password:''
})
