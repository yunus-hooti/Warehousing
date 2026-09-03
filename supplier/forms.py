from django import forms
from .models import  Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name','contact_person','phone_number','email','address','website','national_id']