from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Income, Category, Expense, MyUser, Goal
from .forms import IncomeForm, ExpenseForm, MyUserUpdateForm, MyUserForm, SignInForm,\
                    ExpenseUpdateForm, IncomeUpdateForm, CategoryForm, TechnicalRequestForm,\
                    GoalForm
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
        return render(request, 'mycash/we-are.html')


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
                login(request, user)
                request.session['id'] = user.id
                db = DB()
                db.create_category('Other', user.id)
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
class HistoricalView(View):
    def get(self, request):
        return render(request, 'mycash/expense.html')


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
        nm = 7

        db = DB()
        # Data per day on income and expenses to be visualized visually
        incomes = db.income_month(request.session['id'], nm)
        expenses = db.expense_day(request.session['id'], nd)
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


# List All Goal for each User   [ID]
class GoalView(View):
    template_name = 'mycash/goal.html'

    def get(self, request):
        all_goal = Goal.objects.filter(user_id=request.session['id'])
        db = DB()
        total = float(db.savings_per_user(request.session['id']))

        for goal in all_goal:
            tmp = (float(goal.percentage)*total)/100
            if goal.amount < tmp:
                goal.percentage = 100
            else:
                goal.percentage = round((100*tmp)/float(goal.amount), 2)

        return render(request, self.template_name, {'all_goal': all_goal})


# Create Object Expense to Save in DataBase
class GoalCreate(View):
    form_class = GoalForm
    template_name = 'mycash/manage-goal.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('mycash:overview')

        return render(request, self.template_name, {'form': form})


class GoalUpdate(UpdateView):
    model = Goal
    template_name = 'mycash/manage-goal.html'
    form_class = GoalForm
    success_url = reverse_lazy('mycash:overview')


# Delete Goal
class GoalDelete(DeleteView):
    model = Goal
    success_url = reverse_lazy('mycash:overview')


# List All Category for each User   [ID]
class CategoryIndexView(generic.ListView):
    template_name = 'mycash/overview.html'
    context_object_name = 'all_categories'
    paginate_by = 3

    def get_queryset(self):
        return Category.objects.filter(user_id=self.request.session['id']).order_by('-name')


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
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            db = DB()
            same = db.verify_category(category.name, request.user.id)

            if not same:
                category.save()
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


class MyUserDeleteView(View):
    def get(self, request):
        db = DB()
        db.delete_account(request.session['id'])
        return redirect('mycash:log-out')


class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy('mycash:overview')


class IncomeDelete(DeleteView):
    model = Income
    success_url = reverse_lazy('mycash:overview')


class TechnicalRequestCreate(View):
    form_class = TechnicalRequestForm
    template_name = 'mycash/manage-technical.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            technical_request = form.save(commit=False)
            technical_request.user = request.user
            technical_request.save()
            return redirect('mycash:overview')

        return render(request, self.template_name, {'form': form})


# List All Category for each User   [ID]
class ExpenseIndexView(generic.ListView):
    template_name = 'mycash/expense.html'
    context_object_name = 'all_expense'
    paginate_by = 7

    def get_queryset(self):
        return Expense.objects.filter(user_id=self.request.session['id']).order_by('-date')


# List All Category for each User   [ID]
class IncomeIndexView(generic.ListView):
    template_name = 'mycash/income.html'
    context_object_name = 'all_income'
    paginate_by = 7

    def get_queryset(self):
        return Income.objects.filter(user_id=self.request.session['id']).order_by('-date')