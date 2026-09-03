from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import SupplierForm
from .models import *
from goods.models import Goods


# Create your views here.
@login_required
def list_suppliers(request):
    user = request.user
    if user.is_superuser:
        suppliers = Supplier.objects.all()
        goods = Goods.objects.all()
        user_in_30_days = Supplier.user_in_these_30_days()

        suppliers_count = suppliers.count()

        pagination = Paginator(suppliers, 10)
        pagination_number = request.GET.get('page', 1)

        query_params = request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        suppliers = pagination.get_page(pagination_number)

        return render(request, 'supplier/list_suppliers.html',
                      {'suppliers': suppliers, 'goods': goods, 'user_in_30_days': user_in_30_days,
                       'query_params': query_params, 'suppliers_count': suppliers_count})

    return render(request, 'goods/404.html')


@login_required
def detail_supplier(request, pk):
    user = request.user
    if user.is_superuser:
        supplier = Supplier.objects.get(pk=pk)

        try:
            good_supplier = GoodSupplier.objects.filter(supplier=supplier)
        except:
            good_supplier = None
        return render(request, 'supplier/detail_supplier.html', {'supplier': supplier, 'good_supplier': good_supplier})

    return render(request, 'goods/404.html')


@login_required
def send_supplier(request):
    user = request.user
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            names = [i.company_name for i in Supplier.objects.all()]
            if company_name in names:
                messages.success(request, 'این اسم از قبل وجود دارد')
                return redirect('supplier:list_supplier')
            else:
                supplier_form = form.save(commit=False)
                user.supplier_user = supplier_form
                if request.user.is_superuser:
                    supplier_form.is_active = True
                supplier_form.save()
                user.save()
                return redirect('goods:list_goods')
    else:
        form = SupplierForm()
    return render(request, "supplier/send_supplier.html", {"form": form})
