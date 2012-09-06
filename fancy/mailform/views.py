from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
from django.conf import settings
import settings as appsettings

#from fancy.utils.mail import send_html_mail
from django.utils.html import strip_tags

def send_mail(subject, from_email, recipients, message_html):
    if "mailer" in settings.INSTALLED_APPS:
        from mailer import send_html_mail
        send_html_mail(subject=subject, message=strip_tags(message_html), message_html=message_html, from_email=from_email, recipient_list=recipients)
    else:
        from django.core.mail import EmailMultiAlternatives

        msg = EmailMultiAlternatives(subject, "message_plaintext", from_email, recipients)
        msg.attach_alternative(message_html, "text/html")
        msg.content_subtype = "html"
        msg.send()

def get_mail_content(request):
    tpl = request.POST.get('_tpl', 'default')
    fields = dict((k, v) for k, v in request.POST.items() if k[0] != '_')
    
    return render_to_string("fancy/mailform/mail/%s.html" % tpl, {'fields':fields})

def post_form(request):
    message_html = get_mail_content(request)
    
    from_email = appsettings.FORM_FROM
    recipients = appsettings.FORM_RECIPIENTS
    redirect_to = request.POST.get('_success_url')
    subject = request.POST.get('_subject', appsettings.FORM_SUBJECT)
    
    send_mail(subject, from_email, recipients, message_html)
    
    return redirect(redirect_to)