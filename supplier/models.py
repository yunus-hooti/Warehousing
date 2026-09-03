from django.db import models
from django.utils import timezone

from datetime import timedelta

from goods.models import Goods

# Create your models here.

class Supplier(models.Model):
    company_name = models.CharField(max_length=100, verbose_name='اسم برند یا شرکت')
    contact_person = models.CharField(max_length=100, verbose_name='اسم شخص مسيول یا نماینده')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن')
    email = models.EmailField()
    address = models.CharField(max_length=100, verbose_name='ادرس')
    website = models.URLField(blank=True, null=True, verbose_name='آدرس وبسایت(اختیاری)')
    national_id = models.CharField(max_length=100, verbose_name='شناسه ملی یا کد اقتصادی (برای ثبت رسمی)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ثبت در سیستم')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت فعال یا غیر فعال بود تامین کننده')

    @classmethod
    def user_in_these_30_days(cls, days=30):
        suppliers = cls.objects.all()
        w = 0
        for supplier in suppliers:
            if supplier.created_at > timezone.now() - timedelta(days=days):
                w += 1
        return w



    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'تامین کننده'
        verbose_name_plural = 'تامین کننده ها'


class GoodSupplier(models.Model):
    supplier = models.ForeignKey(Supplier,related_name='suppliers',on_delete=models.CASCADE)
    good = models.ForeignKey(Goods,related_name='suppliers_goods',on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.good.name

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'کالاها'
        verbose_name_plural = "کالاها"






