from django.conf.urls import patterns, url

urlpatterns = patterns('fancy.mailform.views',
    url(r'^post/form/$',
        view='post_form',
        name='mailform_action'
    ),
)
