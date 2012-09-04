from django.conf.urls.defaults import *

urlpatterns = patterns('fancy.payment.views',
    url(r'^$', 'order_form', name="payment_order_form" ),
    url(r'^post$', 'do_payment', name="payment_order_post" ),
    url(r'^basarili/$', 'order_success', name='payment_order_success' ),
    url(r'^(?P<order_hash>[\w\-]+)/$', 'order_detail', name="payment_order_detail" ),
)
