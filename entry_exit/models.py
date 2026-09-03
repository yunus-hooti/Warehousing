from django.db import models
from datetime import timedelta

from django.utils import timezone

from goods.models import Goods
from supplier.models import Supplier, GoodSupplier
from account.models import User


# Create your models here.

class EntryExit(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='entry_exit_good', verbose_name='کالا')
    supplier_good = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='entry_exit_supplier',
                                      verbose_name='تامین کننده')

    good_supplier = models.ForeignKey(GoodSupplier, on_delete=models.CASCADE, related_name='entry_exit_good_supplier',
                                      verbose_name='کالاهای مشتری',null=True,blank=True)
    applicant_person = models.CharField(verbose_name='شخص درخواست دهنده')
    type_of_operation = models.CharField(verbose_name='نوع')
    number = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    registering_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_exit_user',
                                         verbose_name='کاربر ثبت کننده')
    is_active = models.BooleanField(default=False, verbose_name='تایید ورود به انبار')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت')

    @classmethod
    def number_of_arrivals_and_departures_this_month(cls, user, days=30):
        if user.is_superuser:
            entry_exit = cls.objects.all()
        else:
            entry_exit = cls.objects.filter(supplier_good__supplier_user=user)
        w = 0
        for en_ex in entry_exit:
            if en_ex.created_at > timezone.now() - timedelta(days=days):
                w += 1
        return w

    def __str__(self):
        return self.type_of_operation

    class Mate:
        ordering = ('-created_at',)
        indexes = [models.Index(fields=['-created_at'])]
        verbose_name = 'ورود و خروج'
        verbose_name_plural = 'ورود و خروج ها'
