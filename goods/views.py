from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import SearchForm, AddGoodForm, AddCategoriesForm
from .models import *
from supplier.models import Supplier, GoodSupplier
from entry_exit.models import EntryExit
from entry_exit.views import number_of_arrivals_and_departures


# Create your views here.


def total_number_of_supplier():
    suppliers = Supplier.objects.all()
    return len(suppliers)


def running_out_items(goods, request):
    w = 0
    if request.user.is_superuser:
        for item in goods:
            if 0 < item.amount <= 10:
                w += 1
    else:
        for item in goods:
            if 0 < item.good.amount <= 10:
                w += 1
    return w


def warehouse_is_full():
    goods = [i.amount for i in Goods.objects.all()]
    return (sum(goods) / 10000) * 100


@login_required
def list_goods(request, filtered=None):
    supplier = Supplier.objects.get(supplier_user=request.user)
    if request.user.is_superuser:
        goods = Goods.objects.all()
    else:
        goods = GoodSupplier.objects.filter(supplier=supplier)
    category = Category.objects.all()[:5]
    total_amount = len(goods)
    total_supplier = total_number_of_supplier()
    running_items = running_out_items(goods, request)

    pagination = Paginator(goods, 10)
    pagination_number = request.GET.get('page', 1)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    goods = pagination.get_page(pagination_number)

    if filtered:
        if request.user.is_superuser:
            goods = GoodSupplier.objects.filter(good__category__slug__icontains=filtered)
        else:
            goods = GoodSupplier.objects.filter(good__category__slug__icontains=filtered, supplier=supplier)
    warehouse_full = warehouse_is_full()
    return render(request, 'goods/list_goods.html', {'goods': goods, 'category': category, "total_amount": total_amount,
                                                     "total_supplier": total_supplier, 'running_items': running_items,
                                                     'query_params': query_params.urlencode(),
                                                     'warehouse_full': warehouse_full})


def entry_and_exit_of_goods(request, goods_id, supplier):
    if request.user.is_superuser:
        entry = EntryExit.objects.all()
    else:
        entry = EntryExit.objects.filter(good=goods_id, supplier_good=supplier)
    e = []
    for i in entry:
        if i.good.id == goods_id:
            e.append(i)
    e.reverse()

    return e


@login_required
def detail_goods(request, goods_id):
    if request.user.is_superuser:
        good = get_object_or_404(Goods, id=goods_id)
    else:
        good = get_object_or_404(GoodSupplier, id=goods_id)
    supplier = request.user.supplier_user

    entry = entry_and_exit_of_goods(request=request, goods_id=goods_id, supplier=supplier)
    return render(request, 'goods/detail_goods.html', {'good': good, 'entry': entry})


@login_required
def search_goods(request):
    query = None
    result = None
    if request.GET['query'] is not None:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            supplier = Supplier.objects.get(supplier_user=request.user)

            result = GoodSupplier.objects.filter(good__name__icontains=query, supplier=supplier)
            return render(request, 'goods/list_goods.html', {'goods': result})
    return redirect('goods:list_goods')


# def add_goods(request):
#     if request.method == 'POST':
#         form = AddGoodForm(request.POST)
#         if form.is_valid():
#             # --- بخش ۱: مدیریت کالا (جلوگیری از تکرار) ---
#
#             input_name = form.cleaned_data.get('name')
#
#             # جستجو در دیتابیس: آیا کالایی با این کد یا نام وجود دارد؟
#             # (اولویت با کد کالا است)
#             existing_good = None
#
#             # اگر با کد پیدا نشد، با نام چک کن (اختیاری)
#             if not existing_good and input_name:
#                 existing_good = Goods.objects.filter(name=input_name).first()
#
#             if existing_good:
#                 # اگر کالا وجود داشت، از همان استفاده می‌کنیم
#                 final_good = existing_good
#                 print(f"کالای قدیمی پیدا شد: {final_good.name}")
#             else:
#                 # اگر کالا جدید بود، آن را می‌سازیم
#                 # نکته: چون form.save() ممکن است بخواهد دوباره چک کند،
#                 # بهتر است اگر فرم مدل‌فرم است، مستقیم ذخیره کنیم
#
#                     final_good = form.save()
#                     print(f"کالای جدید ساخته شد: {final_good.name}")
#
#             # --- بخش ۲: مدیریت موجودی (GoodSupplier) ---
#
#             supplier_obj = form.cleaned_data['suppliers']  # تامین کننده
#             amount_val = form.cleaned_data['amount']  # تعداد وارد شده
#
#             # استفاده از get_or_create برای مدیریت موجودی
#             # این خط چک می‌کند: آیا این کالا برای این تامین‌کننده رکوردی دارد؟
#             stock_record, created = GoodSupplier.objects.get_or_create(
#                 good=final_good,
#                 supplier=supplier_obj,
#                 number=amount_val  # مقدار اولیه فرضی برای رکورد جدید
#             )
#
#             if created:
#                 # حالت الف: این اولین بار است که این شخص این کالا را می‌آورد
#                 stock_record.number = amount_val
#                 print("رکورد موجودی جدید ایجاد شد.")
#             else:
#                 # حالت ب: قبلاً داشته، پس به تعداد قبلی اضافه می‌کنیم
#                 stock_record.number += amount_val
#                 print("به موجودی قبلی اضافه شد.")
#
#             # ذخیره نهایی موجودی
#             stock_record.save()
#
#             return redirect('goods:list_goods')
#
#     else:
#         form = AddGoodForm()
#
#     return render(request, 'goods/add_goods.html', {'form': form})

@login_required
def add_goods(request):
    if request.user.supplier_user.is_active:
        if request.method == 'POST':
            form = AddGoodForm(request.POST)
            if form.is_valid():
                input_name = form.cleaned_data['name']
                supplier_obj = form.cleaned_data[
                    'suppliers'] if request.user.is_superuser else request.user.supplier_user
                amount_val = form.cleaned_data['amount']
                requester_name = form.cleaned_data['requester_name']
                existing_good = None

                if not existing_good and input_name:
                    existing_good = Goods.objects.filter(name=input_name).first()
                global save_good
                if existing_good:
                    if request.user.is_superuser:
                        goods = existing_good
                        goods.amount += amount_val
                        goods.save()
                        save_good = goods


                    try:
                        if request.user.is_superuser:
                            good_supplier = GoodSupplier.objects.get(good__name=save_good, supplier=supplier_obj)
                            good_supplier.number += amount_val
                            good_supplier.save()
                    except GoodSupplier.DoesNotExist:
                        if request.user.is_superuser:
                            good_supplier = GoodSupplier.objects.create(
                                good=existing_good,
                                supplier=supplier_obj,
                                number=amount_val
                            )
                            good_supplier.save()

                    is_active = True if request.user.is_superuser else False

                    entry_exit = EntryExit.objects.create(good=existing_good, number=amount_val,
                                                          supplier_good=supplier_obj,
                                                          registering_user=request.user,
                                                          type_of_operation='entry',
                                                          applicant_person=requester_name,
                                                          is_active=is_active)
                    entry_exit.save()
                    return redirect('goods:list_goods')

                else:
                    edit_final_good = form.save(commit=False)
                    edit_final_good.amount = 0
                    edit_final_good.save()
                    final_good = edit_final_good
                    if request.user.is_superuser:
                        good = Goods.objects.get(name=input_name)
                        good.amount += amount_val
                        good.save()
                        good_supplier = GoodSupplier.objects.create(
                            good=final_good,
                            supplier=supplier_obj,
                            number=amount_val
                        )
                        good_supplier.save()
                    is_active = True if request.user.is_superuser else False
                    entry_exit = EntryExit.objects.create(good=final_good, number=amount_val,
                                                          supplier_good=supplier_obj,
                                                          registering_user=request.user,
                                                          type_of_operation='entry',
                                                          applicant_person=requester_name,
                                                          is_active=is_active)
                    entry_exit.save()
                    return redirect('goods:list_goods')


        else:
            form = AddGoodForm()
        return render(request, 'goods/add_goods.html', {'form': form})
    else:
        return render(request, 'goods/404.html')


@login_required
def add_categories(request):
    if request.user.supplier_user.is_active:

        if request.method == 'POST':
            form = AddCategoriesForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('goods:list_goods')
        else:
            form = AddCategoriesForm()
        return render(request, 'forms/add_category.html', {'form': form})
    else:
        return render(request, 'goods/404.html')


def running_out_items_list(request):
    w = []
    if request.user.is_superuser:
        goods = Goods.objects.all()
        for item in goods:
            if 0 < item.amount <= 10:
                w.append(item)
    else:
        goods = GoodSupplier.objects.filter(supplier=request.user.supplier_user)
        for item in goods:
            if 0 < item.number <= 10:
                w.append(item)

    return w


@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        suppliers = Supplier.objects.filter(is_active=True)
        goods = GoodSupplier.objects.all()
        entry_exit = EntryExit.objects.all()

    else:
        suppliers = []
        goods = GoodSupplier.objects.filter(supplier__supplier_user=request.user)
        entry_exit = EntryExit.objects.filter(supplier_good__supplier_user=request.user)
    nu_entry_exit = number_of_arrivals_and_departures(request)
    running = running_out_items_list(request=request)
    warehouse_full = warehouse_is_full()
    return render(request, 'goods/dahboard.html', {'goods_count': len(goods), 'suppliers': len(suppliers),
                                                   'nu_entry': nu_entry_exit[0], 'nu_exit': nu_entry_exit[1],
                                                   'running': running, 'entry_exit': entry_exit,
                                                   'warehouse_full': warehouse_full})
