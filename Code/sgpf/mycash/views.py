from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Income, Category, Expense, MyUser
from .forms import IncomeForm, ExpenseForm, MyUserUpdateForm, MyUserForm, SignInForm,\
                    ExpenseUpdateForm, IncomeUpdateForm, CategoryForm
from .sql import DB

from rest_framework.views import APIView
from rest_framework.response import Response

"""
    Class that communicates the templates with the objects in the system
    Class that communicates the templates with the objects in the system, 
    Each view what it does is redirect to its respective template, whether 
    they are co-parameters or without these.
    
    
    All Views that system use in this web page
    IndexView           /mycash/                    [Index Page]
    SignInView          /mycash/sign_in             [Create User to Validate]
    SignUpView          /mycash/sign_up             [Create User to Save DB]
    ChartView           /mycash/chart               [Only View Chart]
    ChartData           /mycash/api/chart/data      [Data APIView Json]
    CategoryIndexView   /mycash/overview            [List Category]
    CategoryDetailView  /mycash/income/<pk>/        [Income-Expense Category]
    IncomeCreate        /mycash/overview            [Create Income to Save DB]
    IncomeUpdate        /mycash/overview            [Update Income in DB]
    ExpenseCreate       /mycash/overview            [Create Expense to Save DB]
    ExpenseUpdate       /mycash/overview            [Update Expense in DB]
"""


# Main view when enter de MyCash Web Page
class IndexView(View):
    def get(self, request):
        return render(request, 'mycash/index.html')


class SignInView(View):
    form = SignInForm()

    def get(self, request):
        context = {'form': self.form}
        return render(request, 'mycash/sign-in.html', context)

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['id'] = user.id
                    return redirect('mycash:overview')
                else:
                    context = {'form': self.form, 'msg': 'User Is Not Active!'}
            else:
                context = {'form': self.form, 'msg': 'Error: Email - Password Invalid'}

            return render(request, 'mycash/sign-in.html', context)


class LogOutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        return redirect('mycash:index')


class SignUpView(View):
    form_class = MyUserForm
    template_name = 'mycash/sign-up.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            # cleaned (normalized) data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(email=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['id'] = user.id
                    return redirect('mycash:overview')

        return render(request, self.template_name, {'form': form})


class UserUpdate(UpdateView):
    model = MyUser
    # fields = ('name', )
    form_class = MyUserUpdateForm
    template_name = 'mycash/profile-edit.html'

    def get_success_url(self):
        return reverse('mycash:profile')


# Class ChartView only use to redirect and see Charts
class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mycash/chart.html', {'customers': 10})


# Class BudgetView only use to redirect and see Budget
class BudgetView(View):
    def get(self, request):
        return render(request, 'mycash/budget.html')


# Class ProfileView only use to redirect and see Profile
class ProfileView(View):
    def get(self, request):
        return render(request, 'mycash/profile.html', {'user': MyUser.objects.get(pk=request.session['id'])})


# Class ChartData to see Default Data Chart
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        income_label = []
        expense_label = []
        income_amount = []
        expense_amount = []

        nd = 7

        db = DB()
        # Data per day on income and expenses to be visualized visually
        incomes = db.income_amount(request.session['id'], nd)
        expenses = db.expense_amount(request.session['id'], nd)
        for inc in incomes:
            income_label.append(str(inc[0]))
            income_amount.append(float(inc[1]))

        for exp in expenses:
            expense_label.append(str(exp[0]))
            expense_amount.append(float(exp[1]))

        data = {
            "income_label": income_label,
            "expense_label": expense_label,
            "income_amount": income_amount,
            "expense_amount": expense_amount,
        }
        return Response(data)


# List All Category for each User   [ID]
class CategoryIndexView(generic.ListView):
    template_name = 'mycash/overview.html'
    context_object_name = 'all_categories'

    def get_queryset(self):
        return Category.objects.filter(user_id=self.request.session['id'])


# Show Income - Expense for each User[ID]
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'mycash/detail.html'


# Create Object Income to Save in DataBase
class IncomeCreate(View):
    def get_initial(self):
        return {'user': self.request.session['id']}

    form_class = IncomeForm
    template_name = 'mycash/manage-income.html'

    # display blank form
    def get(self, request):
        form = self.form_class(request.user, None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('mycash:overview')

        return render(request, self.template_name, {'form': form})


# Create Object Income to Update in DataBase
class IncomeUpdate(UpdateView):
    model = Income
    form_class = IncomeUpdateForm
    template_name = 'mycash/manage-income.html'

    def get_success_url(self):
        return reverse('mycash:overview')


# Create Object Expense to Save in DataBase
class ExpenseCreate(View):
    def get_initial(self):
        return {'user': self.request.session['id']}

    form_class = ExpenseForm
    template_name = 'mycash/manage-expense.html'

    # display blank form
    def get(self, request):
        form = self.form_class(request.user, None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('mycash:overview')

        return render(request, self.template_name, {'form': form})


# Create Object Income to Update in DataBase
class ExpenseUpdate(UpdateView):
    model = Expense
    form_class = ExpenseUpdateForm
    template_name = 'mycash/manage-expense.html'

    def get_success_url(self):
        return reverse('mycash:overview')


# Create Object Expense to Save in DataBase
class CategoryCreate(View):
    form_class = CategoryForm
    template_name = 'mycash/manage-category.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        print("post")
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            print("is valid")
            return redirect('mycash:overview')

        return render(request, self.template_name, {'form': form})


class CategoryUpdate(UpdateView):
    model = Category
    template_name = 'mycash/manage-category.html'
    form_class = CategoryForm
    success_url = reverse_lazy('mycash:overview')


class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('mycash:overview')