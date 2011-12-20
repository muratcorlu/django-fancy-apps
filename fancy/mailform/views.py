from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.conf import settings
import settings as appsettings

if "mailer" in settings.INSTALLED_APPS:
    from mailer import EmailMultiAlternatives
else:
    from django.core.mail import EmailMultiAlternatives

def post_form(request):
    message_html = ""
    for key in request.POST:
        if key[0] != '_': # ignore private fields
            message_html += key + " : " + request.POST.get(key) + "<br />"

    from_email = appsettings.FORM_FROM
    recipients = appsettings.FORM_RECIPIENTS
    redirect_to = request.POST.get('_success_url')
    subject = request.POST.get('_subject', appsettings.FORM_SUBJECT)
    
    msg = EmailMultiAlternatives(subject, "message_plaintext", from_email, recipients)
    msg.attach_alternative(message_html, "text/html")
    msg.content_subtype = "html"
    msg.send()
    
    return redirect(redirect_to)