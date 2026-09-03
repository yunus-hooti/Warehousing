from django.db.models.signals import post_save
from django.dispatch import receiver
from random import randint
from supplier.models import GoodSupplier
from .models import Goods
from entry_exit.models import EntryExit


@receiver(post_save, sender=Goods)
def create_goods_model(sender, instance, created, **kwargs):
    if created:
        cods = ''
        for i in range(8 - len(str(instance.id))):
            cods += str(randint(0, 9))
        cod = f'{instance.id}{cods}'
        instance.good_code = cod
        instance.save()
