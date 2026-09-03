from deep_translator import GoogleTranslator
from django.db import models
from django.utils.text import slugify

from unidecode import unidecode

from .utils import unique_slug_generator


# from supplier.models import Supplier


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            try:
                translator = GoogleTranslator(source='fa', target='en')
                translator_text = translator.translate(self.name)
                self.slug = slugify(translator_text)
            except Exception as e:
                english_text = unidecode(self.name)
                self.slug = slugify(english_text)
        self.slug = unique_slug_generator(self, new_slug=self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Goods(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='goods_category',
                                 verbose_name='دسته بندی')
    name = models.CharField(max_length=100, verbose_name='اسم')
    minimum_stock = models.PositiveIntegerField(default=10, verbose_name="حداقل موجودی برای هشدار")
    slug = models.SlugField(max_length=100, unique=True)
    amount = models.PositiveIntegerField(default=0, verbose_name='تعداد')
    good_code = models.CharField(max_length=10, blank=True, null=True, unique=True, verbose_name='کد کالا (نوشته نشود)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            try:
                translator = GoogleTranslator(source='fa', target='en')
                translator_text = translator.translate(self.name)
                self.slug = slugify(translator_text)
            except Exception as e:
                english_text = unidecode(self.name)
                self.slug = slugify(english_text)
        self.slug = unique_slug_generator(self, new_slug=self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'
