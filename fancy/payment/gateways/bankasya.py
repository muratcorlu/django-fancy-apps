# coding=utf-8
from django.utils.translation import ugettext_lazy as _
from lxml import etree
from xml.etree import ElementTree as ET
import urllib
import urllib2
import logging
import traceback

from fancy.utils.secure_proxy import ConnectHTTPHandler, ConnectHTTPSHandler
# Get an instance of a logger
logger = logging.getLogger('payment.gateway')

class BankAsya(object):
    #vposURL = "https://vpstest.bankasya.com.tr/iposnet/sposnet.aspx?"
    vposURL = "https://vps.bankasya.com.tr/iposnet/sposnet.aspx?"
    merchant_id = None
    merchant_password = None
    
    pos_responses = (   (1001, _('Sistem Hatası')),
                        (1002, _('Veri Tabanı hatası')),
                        (1003, _('Satış işlemi başlatılamadı')),
                        (1004, _('Satış işlemi güncellenemedi')),
                        (1006, _('İlk işlem aranırken hata alındı ( Farklı bir işyerinin kullandığı trnx ıd numarası ile gönderim yapılıyor )')),
                        (1007, _('İlk işlem alınamadı')),
                        (1008, _("CVV2'yi şifrelerken hata alındı")),
                        (1009, _('İş yeri daha önce kullandığı bir işlem numarası gönderdi.')),
                        (1010, _('İşlem iç hata')),
                        (1011, _('İşlem iç hata')),
                        (1043, _("İşlem iptal'de hata alındı")),
                        (1044, _('İşlem iptal iç hata')),
                        (1045, _('İşlem iptal iç hata')),
                        (1046, _('İptal işleminde tutar hatalı')),
                        (1047, _('İşlem tutarı geçersiz.')),
                        (1048, _('İptal edilecek puan geçersiz.')),
                        (1049, _('Geçersiz tutar.')),
                        (1050, _('CVV hatalı')),
                        (1051, _('Kredi Kartı numarası hatalı')),
                        (1052, _('Kredi Kartı son kullanma tarihi hatalı')),
                        (1053, _('İş Yeri numarası hatalı')),
                        (1054, _('İşlem Numarası hatalı')),
                        (1055, _('İşlem tipi hatalı')),
                        (1056, _('Kredi Kartı markası hatalı')),
                        (1057, _('Gönderilen ek bilgiler hatalı')),
                        (1058, _('Gönderilen ek bilgiler hatalı')),
                        (1059, _('Yeniden İade Denemesi')),
                        (1060, _('Hatalı Taksit Sayısı')),
                        (2000, _('Veri Tabanı Hatası')),
                        (2011, _('Uygun Terminal bulunamadı')),
                        (2113, _('Kullanılabilir Terminal bulunamadı')),
                        (2114, _('Seçilen terminal şu anda kullanılamaz')),
                        (2200, _('İş yerinin İşlem için gerekli hakkı yok')),
                        (2201, _('Ön provizyonu gerçekleştirilmemiş işlem. Lütfen önce ön provizyon işlemi yapınız')),
                        (2202, _('İşlem iptal edilemez')),
                        (2300, _('Tanımsız üye iş yeri.')),
                        (3000, _('Banka hostu tarafından desteklenmeyen mesaj tipi.')),
                        (3001, _('Host bağlantı/mesaj hatası. Sistem hata loglarını kontrol ediniz.')),
                        (3003, _('Banka Hostun alınan parametreler yanlış')),
                        (3004, _('Stan oluşturma hatası. Sistem hata loglarını kontrol ediniz. Tekrar deneyiniz')),
                        (3005, _('Banka Hostunda timeout alındı')),
                        (5001, _('İş yeri şifresi yanlış')),
                        (5002, _('İş yeri aktif değil')),
                        (6000, _('Xml hatası')),
                        (6010, _('Tutar sayısal değil')),
                        (6011, _('Para birimi değeri sayısal değil')),
                        (6012, _('Kart numarası sayısal değil')),
                        (6013, _('CVV2 değeri sayısal değil')),
                        (6014, _('Geçersiz son kullanım tarihi')),
                        (6015, _('Tutar 20000 YTLden büyük')),
                        (6016, _('İşlem numarası kabul edilemiyor')),
                        (6020, _('Para tipi sistemde tanımlı değil'))
                    )
    bank_responses = (  (0, _('Approved or completed successfully')),
                        (1, _('Refer to card issuer')),
                        (2, _('Refer to card issuer, special condition')),
                        (3, _('Invalid merchant or service provider')),
                        (4, _('Pick-up card')),
                        (5, _('Do not honour')),
                        (6, _('Error')), # (found only in file update responses)
                        (7, _('Pick up card, special condition')),
                        (8, _('Honour with ID')),
                        (9, _('Try again')),
                        (11, _('Approved')), # (VIP)
                        (12, _('Invalid transaction')),
                        (13, _('Invalid amount')),
                        (14, _('Invalid account number')),
                        (15, _('No such issuer')),
                        (25, _('Unable to locate record on file')),
                        (28, _('Original is denied')),
                        (29, _('Original not found')),
                        (30, _('Format error (switch generated)')),
                        (33, _('Expired card, pick-up')),
                        (36, _('Restricted card, pick-up')),
                        (38, _('Allowable PIN tries exceeded, pick-up')),
                        (41, _('Lost card, Pick-up')),
                        (43, _('Stolen card, pick-up')),
                        (51, _('Insufficient funds')),
                        (52, _('No checking account')),
                        (53, _('No savings account ')),
                        (54, _('Expired card')),
                        (55, _('Incorrect PIN')),
                        (57, _('Transaction not permitted to cardholder')),
                        (58, _('Transaction not permitted to terminal')),
                        (61, _('Exceeds withdrawal amount limit')),
                        (62, _('Restricted card')),
                        (63, _('Security violation')),
                        (65, _('Exceeds withdrawal frequency limit')),
                        (75, _('Allowable number of PIN tries exceeded')),
                        (76, _('Key synchronisation error')),
                        (77, _('Decline of Request – No script available')),
                        (78, _('Unsafe PIN')),
                        (79, _('ARQC failed')),
                        (85, _('Approval of request')), # (for PIN management messages)
                        (91, _('Issuer or switch is inoperative')),
                        (92, _('Financial institution unknown for routing')),
                        (93, _('Invalid BIN')),
                        (96, _('System malfunction')),
                        (98, _('Duplicate Reversal'))
                    )
    

    def __init__(self, id, password):
        self.merchant_id = id
        self.merchant_password = password

    def order_xml(self, data):

        logger.debug(data)
        
        return ('<?xml version="1.0" encoding="ISO-8859-9"?>'
            '<ePaymentMsg VersionInfo="2.0" TT="Request" RM="Direct" CT="Money">'
                '<Operation ActionType="Sale">'
                    '<OpData>'
                        '<MerchantInfo MerchantId="{merchantId}" MerchantPassword="{merchantPassword}" />'
                        '<ActionInfo>'
                            '<TrnxCommon TrnxID="{trnxId}" Protocol="156">'
                                '<AmountInfo Amount="{amount}" Currency="949"/>'
                                '<ProtocolData></ProtocolData>'
                            '</TrnxCommon>'
                            '<PaymentTypeInfo>'
                                '<InstallmentInfo NumberOfInstallments="{installment}"/>'
                            '</PaymentTypeInfo>'
                        '</ActionInfo>'
                        '<PANInfo PAN="{pan}" ExpiryDate="{expiryDate}" CVV2="{cvv2}" BrandID="{brandId}"></PANInfo>'
                        '<OrgTrnxInfo></OrgTrnxInfo>'
                        '<CustomData></CustomData>'
                    '</OpData>'
                '</Operation>'
            '</ePaymentMsg>').format(**data)
    
    def make_request(self, xml):
        params = {}
        params['prmstr'] = xml
        url = self.vposURL + urllib.urlencode(params)
        logger.debug(url)
        req = urllib2.Request( url )
        
        try:
            request = urllib2.urlopen( req )
        except urllib2.HTTPError, err:
            if err.code == 404:
                logger.debug("Page not found!")
            elif err.code == 403:
                logger.debug("Access denied!")
            else:
                logger.debug("Something happened! Error code", err.code)
        except urllib2.URLError, err:
            logger.debug("Some other error happened:", err.reason)
        
        logger.debug(request.code)

        try:
            response_xml = request.read()
            logger.debug(response_xml)
            response = ET.XML(response_xml)
            logger.debug(response)
        except Exception, e:
            logger.debug("Exception: " + str(e))
            logger.debug("Traceback: " + traceback.format_exc())

            response = False

        return response

    def charge(self, cc_number, cvv,  month, year, amount, brand, installment = 0, orderid = None, **kwargs):
        
        data = {
            'merchantId': self.merchant_id,
            'merchantPassword': self.merchant_password,
            'trnxId': '',
            'pan': cc_number,
            'cvv2': cvv,
            'expiryDate': "%d%02d" % (int(year), int(month)),
            'amount': amount,
            'brandId': brand,
            'installment': installment
        }

        request_xml = self.order_xml(data)
        logger.debug(request_xml)

        response_xml = self.make_request(request_xml)

        response = {
            'success': True,
            'status': 0,
            'status_message': '',
            'request_xml': request_xml,
            'response_xml': response_xml
        }

        if not response_xml == False:
            resultcode = response_xml.findall("Operation/OpData/ActionInfo/HostResponse")[0].attrib["ResultCode"]
            if resultcode.isdigit():
                response['status'] = int(resultcode)
                status_message = [resp[1] for resp in self.bank_responses if resp[0] == int(resultcode)]
                if len(status_message) > 0:
                    response['status_message'] = status_message[0]

                if response['status'] > 0:
                    response['success'] = False
        else:
            response['success'] = False
            response['status'] = 100
            response['status_message'] = u'Banka cevabı alınamadı.'

        return response


if __name__ == "__main__":
    print request()

