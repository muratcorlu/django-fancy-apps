from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
from django.conf import settings
import settings as appsettings

if "mailer" in settings.INSTALLED_APPS:
    from mailer import EmailMultiAlternatives
else:
    from django.core.mail import EmailMultiAlternatives

def get_mail_content(request):
    tpl = 'default'
    fields = {}
    
    for key, value in request.POST.items():
        if key[0] != '_': # ignore private fields
            fields[key] = value
    
    if request.POST.get('_tpl'):
        tpl = request.POST.get('_tpl')
    
    return render_to_string("fancy/mailform/mail/%s.html" % tpl, {'fields':fields})

def post_form(request):
    message_html = get_mail_content(request)
    
    from_email = appsettings.FORM_FROM
    recipients = appsettings.FORM_RECIPIENTS
    redirect_to = request.POST.get('_success_url')
    subject = request.POST.get('_subject', appsettings.FORM_SUBJECT)
    
    msg = EmailMultiAlternatives(subject, "message_plaintext", from_email, recipients)
    msg.attach_alternative(message_html, "text/html")
    msg.content_subtype = "html"
    msg.send()
    
    return redirect(redirect_to)