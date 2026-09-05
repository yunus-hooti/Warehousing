# Warehousing

سیستم مدیریت انبار ساخته‌شده با Django برای ثبت و کنترل ورود و خروج کالا.

## امکانات

- مدیریت حساب کاربری (Account)
- ثبت ورود و خروج کالا (Entry/Exit) با فرآیند تأیید مدیر
- مدیریت کالاها (Goods)
- مدیریت تأمین‌کنندگان (Supplier)

## پیش‌نیازها

- Python 3.x
- pip
- (اختیاری ولی توصیه‌شده) virtualenv

## نصب و راه‌اندازی

۱. کلون کردن پروژه:
```bash
git clone https://github.com/yunus-hooti/Warehousing.git
cd Warehousing
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

یک فایل `.env` در ریشه پروژه بساز و مقادیر لازم مثل `SECRET_KEY` را در آن قرار بده.

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
Warehousing/
├── account/       # مدیریت کاربران و احراز هویت
├── entry_exit/    # ثبت ورود و خروج کالا
├── goods/         # مدیریت کالاها
├── supplier/      # مدیریت تأمین‌کنندگان
└── manage.py
```

## تکنولوژی‌ها

- Django
- SQLite (دیتابیس توسعه)

## وضعیت پروژه

این پروژه در حال توسعه است.

## لایسنس

مشخص نشده.
