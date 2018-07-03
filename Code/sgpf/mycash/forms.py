from django import forms
from .models import Income, Expense, MyUser, Category, TechnicalRequest, Goal
from django.contrib.auth.forms import UserChangeForm

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


class MyUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ['name', 'last_name', 'email', 'password']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class User
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),      # last_name field of Class User
            'email': forms.TextInput(attrs={'class': 'form-control'}),          # email field of Class User
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        t = False
        for c in email:
            if c == '@':
                t = True

        if t:
            email_base, provider = email.split('@')
            if not provider == 'mycash.com':
                raise forms.ValidationError("Please make sure you use your @mycash.com email.")
            return email
        else:
            raise forms.ValidationError("Need to enter @mycash.com!!")


# Class UserForm, Use to Create Model User [Objects]data_attrs=('slug',),
class MyUserUpdateForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ['name', 'last_name', 'nickname', 'phone', 'description', 'photo', 'password']

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class User
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),      # last_name field of Class User
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),       # name field of Class User
            'phone': forms.TextInput(attrs={'class': 'form-control'}),          # phone field of Class User
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 20, 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),  # phone field of Class User
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),          # phone field of Class User
        }


# Only form, to capture the data, through POST-GET methods
# It does not represent a model
class SignInForm(forms.Form):
    email = forms.CharField(required=True, label='Email',
                            widget=(forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'})))
    password = forms.CharField(required=True, label='Password',
                               widget=(forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})))


# Class IncomeForm, Use to Create Model Income [Objects]
class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount', 'date', 'category']

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Income
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Income
            'date': DateInput(attrs={'class': 'form-control'}),         # amount field of Class Income
        }

    def __init__(self, user, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


# Class ExpenseForm, Use to Create Model Expense [Objects]
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date', 'category']

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Expense
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Expense
            'date': DateInput(attrs={'class': 'form-control'}),         # amount field of Class Income
        }

    def __init__(self, user, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


# Class IncomeForm, Use to Create Model Income [Objects]
class IncomeUpdateForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount', 'date']

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Income
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Income
            'date': DateInput(attrs={'class': 'form-control'}),         # amount field of Class Income
        }


# Class ExpenseForm, Use to Create Model Expense [Objects]
class ExpenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date']

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Expense
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Expense
            'date': DateInput(attrs={'class': 'form-control'}),         # amount field of Class Income
        }


# Class ExpenseForm, Use to Create Model Expense [Objects]
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # name field of Class Expense
        }


class TechnicalRequestForm(forms.ModelForm):
    class Meta:
        model = TechnicalRequest
        fields = ['description']

        # The fields present in the form
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'cols': 50, 'rows': 15}),  # name field of Class Expense
        }


# Class ExpenseForm, Use to Create Model Expense [Objects]
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name', 'percentage', 'amount']

        # The fields present in the form
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),           # name field of Class Goal
            'percentage': forms.TextInput(attrs={'class': 'form-control'}),     # percentage field of Class Goal
            'amount': forms.TextInput(attrs={'class': 'form-control'}),         # amount field of Class Goal
        }