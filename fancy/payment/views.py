# coding=utf-8
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string
from models import Product, Order, OrderItem, Currency
from django.db import transaction
from datetime import date
import logging
#from django.contrib.localflavor.tr.forms import TRIdentificationNumberField
from validators import isValidTCID
from django import forms
from django.contrib.localflavor.tr.forms import TRPhoneNumberField, TRIdentificationNumberField

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

#from fancy.utils.mail import send_html_mail
from mailer import send_html_mail
from django.utils.html import strip_tags

from gateways.bankasya import BankAsya as payment_gateway
from xml.etree import ElementTree as ET

# Get an instance of a logger
logger = logging.getLogger(__name__)

def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def order_form(request):
    selected_product = request.GET.get('p','')
    if selected_product.isdigit():
        selected_product = int(selected_product)
    else:
        selected_product = 0

    data = {
        'products' : Product.objects.filter(status=1),
        'months' : range(1,13),
        'years' : range(date.today().year, date.today().year + 10),
        'selected_product' : request.GET.get('p'),
        'form_data': request.session.get('_form_data',None),
        'errors': request.session.get('_errors', None),
        'selected_product': selected_product
    }

    return direct_to_template(request, 'fancy/payment/order_form.html', data )

class OrderForm(forms.Form):
    type = forms.ChoiceField(choices=(('bireysel','Bireysel'),('kurumsal','Kurumsal'),))
    
    name = forms.CharField(max_length=50,required=False)
    id = TRIdentificationNumberField(required=False)
    
    vergi_no = forms.CharField(required=False)
    vergi_dairesi = forms.CharField(required=False)
    firm_name = forms.CharField(required=False)

    email = forms.EmailField()
    address = forms.CharField()
    phone = TRPhoneNumberField()

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        fld_type = cleaned_data.get("type")

        if fld_type == 'bireysel':
            name = cleaned_data.get("name")
            id = cleaned_data.get("id")

            if not name:
                self._errors["name"] = self.error_class([u"İsminizi yazınız."])
                del cleaned_data["name"]

            if not id:
                self._errors["id"] = self.error_class([u"TC Kimlik numaranızı yazınız."])
                del cleaned_data["id"]

        if fld_type == 'kurumsal':
            firm_name = cleaned_data.get("firm_name")
            vergi_dairesi = cleaned_data.get("vergi_dairesi")
            vergi_no = cleaned_data.get("vergi_no")

            if not firm_name:
                self._errors["firm_name"] = self.error_class([u"Firma adını yazınız."])
                del cleaned_data["firm_name"]

            if not vergi_dairesi:
                self._errors["vergi_dairesi"] = self.error_class([u"Vergi dairesini yazınız."])
                del cleaned_data["vergi_dairesi"]

            if not vergi_no:
                self._errors["vergi_no"] = self.error_class([u"Vergi numarasını yazınız."])
                del cleaned_data["vergi_no"]

        return cleaned_data

@transaction.commit_on_success
def do_payment(request):
    """
    product     Zeytinyağı (5 lt) (41,5 TL)
    name    Cevahir Hotel
    vergi_dairesi   
    cc_cvcnumber    232
    firm_name   
    phone   0 212 212 12 12
    cc_month    3
    email   muratcorlu@gmail.com
    cc_year     2013
    address     asdsdsdasdsa
    basket  1
    cc_number   
    type    bireysel
    id  a3132312321
    vergi_no
    """
    
    # Validation
    success = True
    errors = {}
    
    orderform = OrderForm(request.POST)
    success = orderform.is_valid()
    if not success:
        errors = orderform.errors

    basket = request.POST.getlist('basket')
    # Sepette urun var mi
    if len(basket) < 1:
        success = False
    
    amount = 0
    for item_id in basket:
        product = Product.objects.get(pk=item_id)
        currency = product.currency
        quantity = int(request.POST.get('frm_quantity_%s' % item_id))
        amount += quantity * product.price
        
    # Fatura tipini ogren
    legal_type = request.POST.get('type')

    if success:
        name = orderform.cleaned_data['name']
        tcid = orderform.cleaned_data['id']
        phone = orderform.cleaned_data['phone']
        address = orderform.cleaned_data['address']
        email = orderform.cleaned_data['email']
        fld_type = orderform.cleaned_data["type"]
        firm_name = orderform.cleaned_data["firm_name"]
        vergi_dairesi = orderform.cleaned_data["vergi_dairesi"]
        vergi_no = orderform.cleaned_data["vergi_no"]

    """    
    # Isim yazilmis mi
    name = request.POST.get('name')
    if not 0 < len(name) < 50:
        success = False
        errors.append({'name':'İsim alanı boş bırakılamaz ve 50 karakterden fazla olamaz.'})
    
    # TCKimlik no gecerli mi
    tcid = request.POST.get('id')
    if not isValidTCID(tcid):
        success = False
        errors.append({'id':'TC Kimlik numarası hatalı'})
    
    # Telefon numarasi gecerli mi
    phone = request.POST.get('phone')
    if len(phone) < 10:
        success = False
        errors.append({'phone':'Telefon numarası boş bırakılamaz ve 10 haneli olmalıdır.'})
    
    # Adres yazilmis mi
    address = request.POST.get('address')
    if len(address) < 5:
        success = False
        errors.append({'address':'Açık adresinizi yazınız.'})
    
    # E-posta adresi gecerli mi
    email = request.POST.get('email')
    """

    # CVC kodu 3 haneli bir sayi mi
    cc_cvcnumber = request.POST.get('cc_cvcnumber')
    if not cc_cvcnumber.isdigit() or not len(cc_cvcnumber) == 3:
        success = False
        errors['cc_cvcnumber'] = ['CVC kodu hatalı',]
    
    # son kullanma tarihi gecerli bir tarih mi
    cc_year = request.POST.get('cc_year','')
    if not cc_year.isdigit() or not int(cc_year) in range(date.today().year, date.today().year + 10):
        success = False
        errors['cc_year'] = ['Kredi kartı son kullanma tarihi(yıl) geçersiz',]

    cc_month = request.POST.get('cc_month', '')
    if not cc_month.isdigit() or not int(cc_month) in range(1,13):
        success = False
        errors['cc_month'] = ['Kredi kartı son kullanma tarihi(ay) geçersiz',]
    
    # Kredi karti numarasi dogru mu (Luhn)
    cc_number = request.POST.get('cc_number').replace(' ', '')
    if not cc_number.isdigit() or not len(cc_number) == 16:
        success = False
        errors['cc_number'] = ['Kredi kartı numarası hatalı.',]

    if success and cc_number[0] == '5':
        brand = 'MASTERCARD'
    else:
        brand = 'VISA'

    # Kredi karti numarasindan kart tipi ogren
    ba_binnumbers = ['402275','402276','416987','402280','441033','477206','515849','527585','524384','531334','552529','529462','547799']
    cc_type = ''
    if success and cc_number[0:6] in ba_binnumbers:
        cc_type = 'bankasya'

    # bankasya karti mi? oyleyse taksit verisini oku
    cc_installment = 0
    installment_options = [7,]

    if cc_type == 'bankasya':
        installment = request.POST.get('cc_installment','')
        if installment.isdigit() and int(installment) in installment_options:
            cc_installment = int(installment)
    
    if success:
        # Odeme verisini kaydet (LOG)
        order = Order()
        if fld_type == 'kurumsal':
            order.name = firm_name
        else:
            order.name = name

        order.email = email
        #order.user_id = models.IntegerField(_('Buyer User ID'),default=0)
        order.invoice_data = {  'address':address,
                                'type': '',
                                'firm_name': firm_name,
                                'vergi_dairesi': vergi_dairesi,
                                'vergi_no': vergi_no }

        order.address_data = {  'address':address,
                                'phone':phone}
                                
        order.payment_data = {  'cc_number':"%s **** **** %s" % (cc_number[:4], cc_number[-4:]),
                                'brand': brand, 
                                'last_usage': "%s/%s" % (cc_month, cc_year),
                                'installment': (cc_installment != None),
                                'installment_count': cc_installment,
                                'request_xml': '',
                                'response_xml': '',
                                }
        order.status = 0
        order.total_price = amount
        order.currency = currency.name
        order.currency_id = currency.id
        order.save()
        
        for item_id in basket:
            product = Product.objects.get(pk=item_id)
            quantity = int(request.POST.get('frm_quantity_%s' % item_id))
            total = quantity * product.price
            
            item = OrderItem(order=order,
                            product_id=product.id,
                            name=product.name,
                            quantity=quantity,
                            price=product.price,
                            total_price=total,
                            currency=currency.name,
                            currency_id=currency.id)
            item.save()
        
        order.save()
        
        # Odeme talebini bankaya gonder (LOG)
        gateway = payment_gateway(id=settings.PAYMENT_GATEWAY_SETTINGS['merchant_id'], 
                                password=settings.PAYMENT_GATEWAY_SETTINGS['merchant_password'])

        
        response = gateway.charge(cc_number=cc_number, 
                                    cvv=cc_cvcnumber,  
                                    month=cc_month, 
                                    year=cc_year, 
                                    amount=order.total_price, 
                                    brand=brand, 
                                    installment=cc_installment,
                                    orderid=None)
        
        
        if response['success'] == False:
            # Hata olursa odeme verisini tekrar sil (LOG)
            order.delete()
            success = False
            errors['cc_number'] = [response['status_message'],]
        else:
            logger.info(response)
            order.payment_data['request_xml'] = response['request_xml']
            order.payment_data['response_xml'] = ET.tostring(response['response_xml'])
            order.save()
    

    # Hata yoksa siparis bilgisini yoneticiye ve kullaniciya mail at (LOG)
    
    #return HttpResponse('success')
    if success:
        message_html = render_to_string("fancy/payment/mail_order.html", {'order':order})
        
        send_html_mail(subject='Ödeme alındı!', message=strip_tags(message_html), message_html=message_html, from_email=settings.PAYMENT_MAIL_FROM, recipient_list=settings.PAYMENT_MAIL_RECIPIENTS)

        message_html = render_to_string("fancy/payment/mail_order_user.html", {'order':order})

        send_html_mail(subject='Ödemeniz alındı!', message=strip_tags(message_html), message_html=message_html, from_email=settings.PAYMENT_MAIL_FROM, recipient_list=[email])

        if request.session.get('_form_data', None):
            del request.session['_form_data']
        if request.session.get('_errors', None):
            del request.session['_errors']

        request.session['order_id'] = order.id
        return redirect('payment_order_success')
    else:
        request.session['_form_data'] = request.POST
        request.session['_errors'] = errors
        return redirect('payment_order_form')

def order_detail(request, order_hash):
    order = get_object_or_404(Order,order_hash=order_hash)
    
    return direct_to_template(request, 'fancy/payment/order_detail.html', { 'order': order} )

def order_success(request):
    order_id = request.session.get('order_id',0)
    order = get_object_or_404(Order,pk=order_id)

    return direct_to_template(request, 'fancy/payment/order_success.html', { 'order': order})
