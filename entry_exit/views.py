from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from weasyprint import HTML

from .models import EntryExit
from .forms import EntryExitSuperUserForm, EntryExitUserForm, SearchForm
from goods.models import Goods
from supplier.models import Supplier, GoodSupplier
from goods.utils import send_low_stock_email


# Create your views here.

@login_required
def true_is_good_entry_exit(request, entry_exit_id):
    if request.user.is_superuser:
        entry_exit = get_object_or_404(EntryExit, pk=entry_exit_id)

        good = entry_exit.good
        supplier = entry_exit.supplier_good
        number = entry_exit.number
        goods = Goods.objects.get(name=good)
        if entry_exit.type_of_operation == 'entry' and entry_exit.is_active is False:
            goods.amount += number
            goods.save()
            good_supplier, created = GoodSupplier.objects.get_or_create(
                good=good,
                supplier=supplier,
            )
            good_supplier.number += number
            good_supplier.save()

            entry_exit.good_supplier = good_supplier
            entry_exit.is_active = True
            entry_exit.save()

            return redirect('entry_exit:list_entry_exit')
        elif entry_exit.type_of_operation == 'exit' and entry_exit.is_active is True:
            entry_exit.is_active = False
            entry_exit.save()
            good_supplier = get_object_or_404(GoodSupplier, good__name=good, supplier__company_name=supplier)
            goods.amount += number
            goods.save()
            good_supplier.number += number
            good_supplier.save()
            return redirect('entry_exit:list_entry_exit')

        elif entry_exit.type_of_operation == 'exit' and entry_exit.is_active is False:
            goods.amount -= number
            goods.save()
            good_supplier, created = GoodSupplier.objects.get_or_create(
                good=good,
                supplier=supplier,
            )
            good_supplier.number -= number
            good_supplier.save()

            entry_exit.good_supplier = good_supplier
            entry_exit.is_active = True
            entry_exit.save()
            return redirect('entry_exit:list_entry_exit')


        else:
            if entry_exit.is_active:
                entry_exit.is_active = False
                entry_exit.save()
            good_supplier = get_object_or_404(GoodSupplier, good__name=good, supplier__company_name=supplier)
            goods.amount -= number
            goods.save()
            good_supplier.number -= number
            good_supplier.save()
            return redirect('entry_exit:list_entry_exit')
    return None


@login_required
def entry_exit_entry(request):
    if request.user.supplier_user.is_active:
        if request.method == 'POST':
            form = EntryExitSuperUserForm(request.POST) if request.user.is_superuser else EntryExitUserForm(
                request.POST, user=request.user)
            if form.is_valid():
                operation = form.save(commit=False)
                good = form.cleaned_data['good']
                number = form.cleaned_data['number']
                supplier = form.cleaned_data[
                    'supplier_good'] if request.user.is_superuser else request.user.supplier_user
                operation.type_of_operation = 'entry'
                operation.registering_user = request.user
                operation.is_active = True if request.user.is_superuser else False
                if not request.user.is_superuser:
                    operation.supplier_good = supplier
                operation.save()
                if request.user.is_superuser:
                    goods = Goods.objects.get(name=good)
                    goods.amount += number
                    goods.save()
                    suppliers = Supplier.objects.get(company_name=supplier)
                    GoodSupplier.objects.get_or_create(good=goods, supplier=suppliers, number=number)
                    return redirect('goods:list_goods')
                else:
                    messages.success(request, 'درخواست به انبار ارسال شد')
                    return redirect('goods:list_goods')
        else:
            form = EntryExitSuperUserForm() if request.user.is_superuser else EntryExitUserForm(user=request.user)
        return render(request, 'forms/entry_exi_entry.html', {'form': form, })
    else:
        return render(request, 'goods/404.html')


@login_required
def entry_exit_exit(request):
    if request.user.supplier_user.is_active:
        if GoodSupplier.objects.filter(supplier__company_name=request.user.supplier_user.company_name).exists():
            pass
        else:
            messages.success(request, 'شما هنوز کالای در انبار ندارید نمیتوانید کالا خارح کنید')
            return redirect('entry_exit:list_entry_exit')
        if request.method == 'POST':
            form = EntryExitSuperUserForm(request.POST) if request.user.is_superuser else EntryExitUserForm(
                request.POST, user=request.user)
            if form.is_valid():
                operation = form.save(commit=False)
                good = form.cleaned_data['good']
                number = form.cleaned_data['number']
                supplier = form.cleaned_data[
                    'supplier_good'] if request.user.is_superuser else request.user.supplier_user
                goods = Goods.objects.get(name=good)
                goods_supplier = GoodSupplier.objects.filter(supplier=supplier, good=good).first()
                w = [i.number for i in GoodSupplier.objects.all() if i.supplier.company_name == supplier.company_name]
                if w:
                    if goods_supplier.number >= number:

                        operation.type_of_operation = 'exit'
                        operation.registering_user = request.user
                        operation.is_active = True if request.user.is_superuser else False
                        if not request.user.is_superuser:
                            operation.supplier_good = supplier
                        operation.save()
                        send_low_stock_email(goods_supplier)
                        if request.user.is_superuser:
                            goods.amount -= number
                            goods.save()
                            goods_supplier.number -= number
                            goods_supplier.save()

                        messages.success(request, 'خروج ثبت شد')
                        return redirect('goods:list_goods')

                    else:
                        form.add_error('number',
                                       f'موجودی کالای {goods.name}, برای این کاربر  {goods_supplier.number} است ')
                        return render(request, 'forms/entry_exit_exit.html', {'form': form})
                else:
                    messages.success(request, 'این شخص این کالا را در انبار ندارد')
                    return redirect('goods:list_goods')

        else:
            form = EntryExitSuperUserForm() if request.user.is_superuser else EntryExitUserForm(user=request.user)
        return render(request, 'forms/entry_exit_exit.html', {'form': form})
    else:
        return render(request, 'goods/404.html')


@login_required
def generate_pdf_receipt(request, pk):
    if request.user.is_superuser:
        entry_exit = get_object_or_404(EntryExit, pk=pk)

        doc_type = "رسید ورود به انبار" if entry_exit.type_of_operation == 'entry' else "حواله خروج از انبار"
        context = {
            'tx': entry_exit,
            'doc_type': doc_type,
            'user': request.user.username
        }
        html_string = render_to_string('entry_exit/pdf_receipt.html', context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        filename = f"receipt_{pk}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        response.write(result)

        return response
    else:
        try:
            entry_exit = get_object_or_404(EntryExit, pk=pk, supplier_good=request.user.supplier_user)
        except:
            return render(request, 'goods/404.html')

        doc_type = "رسید ورود به انبار" if entry_exit.type_of_operation == 'entry' else "حواله خروج از انبار"
        context = {
            'tx': entry_exit,
            'doc_type': doc_type,
            'user': request.user.username
        }
        html_string = render_to_string('entry_exit/pdf_receipt.html', context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        result = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        filename = f"receipt_{pk}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        response.write(result)

        return response


def number_of_arrivals_and_departures(request):
    if request.user.is_superuser:
        list_entry_exit_all = EntryExit.objects.all()
    else:
        list_entry_exit_all = EntryExit.objects.filter(supplier_good__supplier_user=request.user)
    login = 0
    departures = 0

    for i in list_entry_exit_all:
        if str(i.created_at)[0:10] == str(timezone.now())[0:10]:
            if i.type_of_operation == 'entry':
                login += 1
            else:
                departures += 1
    return [login, departures]


@login_required
def list_entry_exit(request, filter=None):
    if request.user.is_superuser:
        list_entry_exit_all = EntryExit.objects.all().order_by('-created_at')
    else:
        list_entry_exit_all = EntryExit.objects.filter(supplier_good__supplier_user=request.user).order_by(
            '-created_at')
    number_entry_exit = number_of_arrivals_and_departures(request)
    in_these_30_days = EntryExit.number_of_arrivals_and_departures_this_month(user=request.user)

    pagination = Paginator(list_entry_exit_all, 10)
    pagination_number = request.GET.get('page', 1)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    list_entry_exit_all = pagination.get_page(pagination_number)

    if filter:
        list_entry_exit_all = EntryExit.objects.filter(type_of_operation__icontains=filter,
                                                       supplier_good=request.user.supplier_user).order_by('-created_at')
    return render(request, 'entry_exit/list_entry_exit.html',
                  {'list_entry_exit': list_entry_exit_all, 'login': number_entry_exit[0],
                   'departures': number_entry_exit[1], 'days30': in_these_30_days, 'query_params': query_params})


@login_required
def detail_entry_exit(request, entry_id):
    entry_exit = get_object_or_404(EntryExit, id=entry_id)
    return render(request, 'entry_exit/detail_entry_exit.html', {'entry_exit': entry_exit})


@login_required
def search_goods(request):
    query = None
    result = None
    if request.GET['query'] is not None:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result = EntryExit.objects.filter(good__name__icontains=query)
            return render(request, 'entry_exit/list_entry_exit.html', {'list_entry_exit': result})
    return redirect('entry_exit:list_entry_exit')


@require_GET
def load_suppliers_for_good(request):
    """
    بر اساس ID کالا، تامین‌کنندگانی که آن کالا را موجود دارند برمی‌گرداند.
    پارامتر GET: good_id
    خروجی: JSON لیستی از دیکشنری‌ها با کلیدهای 'id' و 'name'
    """
    good_id = request.GET.get('good_id')
    if not good_id:
        return JsonResponse([], safe=False)

    suppliers_qs = GoodSupplier.objects.filter(
        good_id=good_id,
        number__gt=0
    ).select_related('supplier').values(
        'supplier__id', 'supplier__company_name'
    ).distinct().order_by('supplier__company_name')
    data = [
        {'id': item['supplier__id'], 'name': item['supplier__company_name']}
        for item in suppliers_qs
    ]
    return JsonResponse(data, safe=False)
