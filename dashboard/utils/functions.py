import logging

import requests
from django.conf import settings

from dashboard.models import Sms
from setup.models import SysConfig

logger = logging.getLogger("django")


def send_sms(sms_id):
    config = SysConfig.objects.first()
    sms = Sms.objects.filter(id=sms_id).first()
    if not sms or not config.send_sms:
        sms.response = "SMS disabled"
        sms.save()
        return False
    number = sms.number
    message = sms.message
    sender_id = config.sms_sender_id
    url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key={settings.ARKESEL_API}&to={number}&from={sender_id}&sms={message}"
    try:
        response = requests.get(url)
    except Exception as e:
        logger.error(str(e))
        return None
    sms.response = response.text
    if response.json().get("code") == 'ok':
        sms.success = True
    if hasattr(response, "json"):
        sms.status_message = response.json().get("message")
    sms.save()
    return sms
