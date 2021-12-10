from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import WeekPlan, Sale

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class PlanForm(forms.ModelForm):
    class Meta:
        model = WeekPlan
        fields = ('seller', 'amount')

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('seller', 'product')

class DateForm(forms.Form):
    from_date = forms.DateTimeField(label='Начала периода')
    to_date = forms.DateTimeField(label='Конец периода')
