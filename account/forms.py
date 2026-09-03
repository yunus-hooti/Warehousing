from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .models import User

class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fieldsets = ['username','first_name','last_name','','phon','email','address','supplier_user','is_active','is_staff','is_superuser','created_at','updated_at']


class ChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fieldsets = ['username','first_name','last_name','','phon','email','address','is_active','is_staff','is_superuser','created_at','updated_at']


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput)
    password2 = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','phon','email','address']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('رمز ها یکی نیستن')
        return cd['password1']

    def clean_phon(self):
        phon = self.cleaned_data['phon']
        if phon.isdigit():
            if len(phon)==11:
                if User.objects.filter(phon=phon).exists():
                    raise forms.ValidationError('این شماره از قبل وجود دارد')
                return phon
            else:
                raise forms.ValidationError('شماره بایذ ۱۱ رقم است')

        else:
            raise forms.ValidationError('شماره باید عدد باشد')





