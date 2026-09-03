from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import threading


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name, aloow_unicode=True)
    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{rendstr}".format(
            slug=slug, rendstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def random_string_generator(size=10, chars='abcdefghijklmnopqrstuvwxyz0123456789'):
    import random
    return ''.join(random.choice(chars) for _ in range(size))


def send_low_stock_email(stock_record):
    amount = stock_record.good.amount
    minimum_stock = stock_record.good.minimum_stock
    emile_supplier = stock_record.supplier.email

    if amount <= minimum_stock:
        subject = f"⚠️ هشدار موجودی: {stock_record.good.name}"

        # پیام متنی ساده
        message = f"""
                سلام {stock_record.supplier.company_name}،

                موجودی کالای '{stock_record.good.name}' در انبار کاهش یافته است.

                موجودی فعلی: {amount} عدد
                حداقل تعیین شده: {minimum_stock} عدد

                لطفاً جهت شارژ مجدد اقدام نمایید.
                """
        try:
            email_thread = threading.Thread(
                target=send_mail,
                args=(
                    subject,
                    message,
                    'mostafa.hooti789@gmail.com',
                    [emile_supplier],
                )
            )
            email_thread.start()
            print(f"ایمیل هشدار برای {stock_record.good.name} ارسال شد.")
        except Exception as e:
            print(f"خطا در ارسال ایمیل: {e}")
