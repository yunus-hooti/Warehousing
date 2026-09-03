from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginUserForm, RegistrationForm
from supplier.models import GoodSupplier
from entry_exit.models import EntryExit


# Create your views here.

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('goods:dashboard_view')
            else:
                messages.success(request, 'نام کاربری یا رمز عبوز اشتباه است', extra_tags='wrong')
    else:
        form = LoginUserForm()
    return render(request, 'account/login_user.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'شما خارج شدید')
    return redirect('account:login')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('account:login')
    else:
        form = RegistrationForm()
    return render(request, 'account/registration.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    goods = GoodSupplier.objects.filter(supplier=user.supplier_user)
    entry_exit = EntryExit.objects.filter(supplier_good=user.supplier_user)
    return render(request,'account/profile.html', {'user': user, 'goods': goods,
                                                   'entry_exit': entry_exit,'goods_count':goods.count(),'transactions_count':entry_exit.count()})