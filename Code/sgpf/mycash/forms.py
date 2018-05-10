from django import forms
# from .varglobal import IdUserLogged
from .models import Income, Expense, User, Category

""" 
    creation of the ModelForm forms, this is super useful to update,
    delete and insert records in their respective models
    
        [CRUD] View 
            Create View
            Retrieve View
            Update View
            Delete View
"""


class DateInput(forms.DateInput):
    input_type = 'date'


# Class UserForm, Use to Create Model User [Objects]data_attrs=('slug',),
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        user_type = forms.ModelChoiceField(queryset=User.objects.filter(id=1), empty_label=None, to_field_name="user_type")
        # phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial="NULL")
        fields = '__all__'

        # The fields present in the form
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
        category = forms.ModelChoiceField(queryset=Category.objects.filter(user=1), empty_label=None, to_field_name="category")
        fields = '__all__'

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Income
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Income
            'date': DateInput(attrs={'class': 'form-control'}),         # amount field of Class Income
            'user': forms.TextInput(attrs={'class': 'form-control'}),  # amount field of Class Income
        }


# Class ExpenseForm, Use to Create Model Expense [Objects]
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        category = forms.ModelChoiceField(queryset=Category.objects.filter(user=1), empty_label=None, to_field_name="category")
        fields = '__all__'

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Expense
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Expense
            'date': DateInput(attrs={'class': 'form-control'}),         # amount field of Class Income
            'user': forms.TextInput(attrs={'class': 'form-control'}),  # amount field of Class Income
        }


# Only form, to capture the data, through POST-GET methods
# It does not represent a model
class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))