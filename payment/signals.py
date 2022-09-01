from django.db.models.signals import post_save
from django.dispatch import receiver

from azbankgateways.models import Bank
from order.models import Order


@receiver(post_save, sender=Bank)
def BankSaveSignal(sender, instance, created, *args, **kwargs):
    if created:
        pass
