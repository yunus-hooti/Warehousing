from django import forms

from .models import EntryExit
from supplier.models import GoodSupplier


class EntryExitSuperUserForm(forms.ModelForm):
    class Meta:
        model = EntryExit
        fields = ['good', 'supplier_good', 'applicant_person', 'number']


class EntryExitUserForm(forms.ModelForm):
    class Meta:
        model = EntryExit
        fields = ['good_supplier', 'applicant_person', 'number']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['good_supplier'].queryset = GoodSupplier.objects.filter(supplier=self.user.supplier_user)




class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)