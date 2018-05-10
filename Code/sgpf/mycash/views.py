from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.views import generic
from .varglobal import idUserLogged
from .models import Income, Category, Expense, User
from .forms import IncomeForm, ExpenseForm, UserForm, LoginForm
from .sql import DB

from rest_framework.views import APIView
from rest_framework.response import Response

"""
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


# Create Object User to Validate
class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {'form': form}
        return render(request, 'mycash/sign_in.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            password = request.POST.get('password')

        db = DB()
        idUserLogged = int(db.validate_user(email,password))

        if idUserLogged == 0:
            return redirect('mycash:sign-in')
        else:
            return redirect('mycash:overview')


# Create Object User to Save in DataBase
class UserCreate(CreateView):
    model = User
    form_class = UserForm
    initial = {'phone': '----', 'state': 'True', 'user_type': 1}

    template_name = 'mycash/sign_up.html'

    def get_success_url(self):
        return reverse('mycash:overview')


class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
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
        return render(request, 'mycash/profile.html', {'user': User.objects.get(pk=idUserLogged)})


# Class ChartData to see Default Data Chart
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        income_label = []
        expense_label = []
        income_amount = []
        expense_amount = []

        nd = 3

        db = DB()
        incomes = db.income_amount(idUserLogged, nd)
        expenses = db.expense_amount(idUserLogged, nd)
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
        return Category.objects.filter(user_id=idUserLogged)
        # return Category.objects.all()


# Show Income - Expense for each User[ID]
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'mycash/detail.html'


# Create Object Income to Save in DataBase
class IncomeCreate(CreateView):
    model = Income
    form_class = IncomeForm
    initial = {'user': idUserLogged}
    template_name = 'mycash/manage_income.html'

    def get_success_url(self):
        return reverse('mycash:overview')


# Create Object Income to Update in DataBase
class IncomeUpdate(UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'mycash/manage_income.html'

    def get_success_url(self):
        return reverse('mycash:overview')


# Create Object Expense to Save in DataBase
class ExpenseCreate(CreateView):
    model = Expense
    form_class = ExpenseForm
    initial = {'user': idUserLogged}
    template_name = 'mycash/manage_expense.html'

    def get_success_url(self):
        return reverse('mycash:overview')


# Create Object Income to Update in DataBase
class ExpenseUpdate(UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'mycash/manage_expense.html'

    def get_success_url(self):
        return reverse('mycash:overview')