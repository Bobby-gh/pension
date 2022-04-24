import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Application, ControllerForm, Sms
from dashboard.utils.functions import send_sms

logger = logging.getLogger("django")


@receiver(post_save, sender=Sms)
def signal_send_sms(sender, instance, created, **kwargs):
    if created:
        res = send_sms(instance.id)
        logger.info(res.response)


@receiver(post_save, sender=Application)
def signal_create_controller_form(sender, instance, created, **kwargs):
    _, found = ControllerForm.objects.get_or_create(application=instance)
    if not found:
        logger.info("Creater controller form for application {}".format(
            instance.id))
