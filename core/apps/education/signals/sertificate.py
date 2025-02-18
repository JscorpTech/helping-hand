from django.db.models.signals import post_save
from django.dispatch import receiver

from core.apps.education.models import SertificateModel
from core.apps.education.services.sertificate import SertificateService


@receiver(post_save, sender=SertificateModel)
def generate_sertificate(sender, instance, created, **kwargs):
    if created:
        sertificate_service = SertificateService(user=instance.user)
        instance.file = sertificate_service.generate()
        instance.save()
