from django import forms
from .models import Goods,Category
from supplier.models import Supplier


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


class AddGoodForm(forms.ModelForm):
    suppliers = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        label='تامین کننده',
        required=False,
    )
    requester_name = forms.CharField(max_length=100)

    class Meta:
        model = Goods
        fields = ['category', 'name','requester_name','suppliers', 'amount']


class AddCategoriesForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
