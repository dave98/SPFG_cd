from django import forms
from .models import Income, Expense, User, Category

"""
    [CRUD] View 
        Create View
        Retrieve View
        Update View
        Delete View
"""


# Class UserForm, Use to Create Model User [Objects]
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class User
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),      # last_name field of Class User
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),   # password field of Class User
            'email': forms.TextInput(attrs={'class': 'form-control'}),          # email field of Class User
            'phone': forms.TextInput(attrs={'class': 'form-control'}),          # phone field of Class User
            'state': forms.TextInput(attrs={'class': 'form-control'}),          # state field of Class User
        }


# Class IncomeForm, Use to Create Model Income [Objects]
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Income
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Income
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),  # category field of Class Income
        }


# Class ExpenseForm, Use to Create Model Expense [Objects]
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Expense
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Expense
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),  # category field of Class Expense
            # 'category': forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="(Nothing)"),
        }