from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from dashboard.models import Sms
from dashboard.utils.functions import send_sms

logger = logging.getLogger("django")


@receiver(post_save, sender=Sms)
def signal_send_sms(sender, instance, created, **kwargs):
    if created:
        res = send_sms(instance.id)
        logger.info(res.response)
