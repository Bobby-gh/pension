import requests

from dashboard.models import Sms
from django.conf import settings
from setup.models import SysConfig


def send_sms(sms_id):
    sms = Sms.objects.filter(id=sms_id).first()
    if not sms: return
    number = sms.number
    message = sms.message
    sender_id = SysConfig.objects.first().sms_sender_id
    url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key={settings.ARKESEL_API}&to={number}&from={sender_id}&sms={message}"
    response = requests.get(url)
    sms.response = response.text
    if response.json().get("code") == 'ok':
        sms.success = True
    if hasattr(response, "json"):
        sms.status_message = response.json().get("message")
    sms.save()
    return sms
