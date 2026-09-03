# Store

یک فروشگاه اینترنتی ساخته‌شده با Django برای فروش محصولات فیزیکی (پوشاک، اکسسوری و...).

## امکانات

- مدیریت حساب کاربری (Account)
- سبد خرید (Cart)
- کاتالوگ محصولات (Catalog)
- کد تخفیف (Coupon)
- ثبت و مدیریت سفارش (Order)
- پرداخت (Payment) — پرداخت آنلاین از طریق درگاه زرین‌پال (Zarinpal)
- ترجمه خودکار محتوا (deep-translator)
- API (برای اتصال به اپ موبایل یا فرانت‌اند جدا) با Django REST Framework

## پیش‌نیازها

- Python 3.x
- pip
- (اختیاری ولی توصیه‌شده) virtualenv

## نصب و راه‌اندازی

۱. کلون کردن پروژه:
```bash
git clone https://github.com/yunus-hooti/store.git
cd store
```

۲. ساخت و فعال‌سازی محیط مجازی:
```bash
python -m venv venv
source venv/bin/activate   # لینوکس / مک
venv\Scripts\activate      # ویندوز
```

۳. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

۴. تنظیم متغیرهای محیطی:

یک فایل `.env` در ریشه پروژه بساز (نمونه‌ی آن در `.env.example` موجود است) و مقادیر لازم مثل `SECRET_KEY` را در آن قرار بده.

۵. اجرای migration ها:
```bash
python manage.py migrate
```

۶. ساخت کاربر ادمین (اختیاری):
```bash
python manage.py createsuperuser
```

۷. اجرای سرور توسعه:
```bash
python manage.py runserver
```

پروژه روی آدرس `http://127.0.0.1:8000/` در دسترس خواهد بود.

## ساختار پروژه

```
store/
├── account/      # مدیریت کاربران و احراز هویت
├── cart/         # سبد خرید
├── catalog/      # محصولات و دسته‌بندی‌ها
├── coupon/       # کد تخفیف
├── order/        # سفارش‌ها
├── payment/      # پرداخت
├── api/          # REST API
└── manage.py
```

## تکنولوژی‌ها

- Django 5.2.7
- Django REST Framework 3.17.1
- Zarinpal Python SDK (درگاه پرداخت)
- Pillow (پردازش تصاویر)
- deep-translator (ترجمه خودکار)
- pytest (تست)
- SQLite (دیتابیس توسعه)

## وضعیت پروژه

این پروژه در حال توسعه است (MVP).

## لایسنس

مشخص نشده.
