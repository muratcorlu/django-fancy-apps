from django.conf.urls.defaults import *

urlpatterns = patterns('fancy.mailform.views',
    url(r'^post/form/$',
        view='post_form',
        name='mailform_action'
    ),
)
