from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View
from django.views import generic
from .models import Income, Category, Expense, User
from .forms import IncomeForm, ExpenseForm, UserForm

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
class SignInView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'mycash/sign_in.html'

    def get_success_url(self):
        return reverse('mycash:overview')


# Create Object User to Save in DataBase
class SignUpView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'mycash/sign_up.html'

    def get_success_url(self):
        return reverse('mycash:overview')


# Class ChartView only use to redirect and see Charts
class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mycash/chart.html', {'customers': 10})


# Class ChartData to see Default Data Chart
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        default_items = [1, 4, 2, 4, 6, 8, 3]
        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)


# List All Category for each User   [ID]
class CategoryIndexView(generic.ListView):
    template_name = 'mycash/overview.html'
    context_object_name = 'all_income_categories'

    def get_queryset(self):
        return Category.objects.all()


# Show Income - Expense for each User[ID]
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'mycash/detail.html'


# Create Object Income to Save in DataBase
class IncomeCreate(CreateView):
    model = Income
    form_class = IncomeForm
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