from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.views import generic
from .utils import render_to_pdf, Day

from django.core.urlresolvers import reverse, reverse_lazy
from .models import Income, Category, Expense, MyUser, Goal
from .forms import IncomeForm, ExpenseForm, MyUserUpdateForm, MyUserForm, SignInForm,\
                    ExpenseUpdateForm, IncomeUpdateForm, CategoryForm, TechnicalRequestForm,\
                    GoalForm

from .sql import DB
from datetime import datetime
from django.db.models import Func, Sum, Q

from rest_framework.views import APIView
from rest_framework.response import Response

"""
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


# Sign In view to enter the system
# get(): When we direct to 'mycash/sign-in.html', it shows us the form SignInForm
# post(): When we send the form's data, it first check if the data are valid,
# then it authenticate the email and password in the database, if the user exists,
# then if user is active, we then login, and redirect to 'mycash:overview'
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


# The LogOutView when is called redirects to 'mycash:index'
class LogOutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        return redirect('mycash:index')


# The SignUpView let you register in the system
# It has the form MyUserForm and is related to the html file 'mycash/sign-up.html'
# When we send the form, first it check if the values area valid, then
# it checks if the user exist in the database, if it does, then we dont create
# the user in the database, if it doesn't we save the data of the new user.
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
            email = form.clean_email()
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                request.session['id'] = user.id
                Category.create('Work', user).save()
                Category.create('Home', user).save()
                Category.create('Furniture', user).save()
                return redirect('mycash:overview')

        return render(request, self.template_name, {'form': form})


# This class is called when we go to "mycash/manage-user.html"
# Update the user's data with the help of the model MyUser,
# for this we need to fill the form MyUserUpdateForm
# When we send the form, this redirects us to the profile view.
class UserUpdate(UpdateView):
    model = MyUser
    # fields = ('name', )
    form_class = MyUserUpdateForm
    template_name = 'mycash/manage-user.html'

    def get_success_url(self):
        return reverse('mycash:profile')


# Class ProfileView only use to redirect and see Profile
class ProfileView(View):
    def get(self, request):
        return render(request, 'mycash/profile.html', {'user': MyUser.objects.get(pk=request.session['id'])})


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
                goal.adv_percentage = 100
            else:
                goal.adv_percentage = round((100*tmp)/float(goal.amount), 2)

        return render(request, self.template_name, {'all_goal': all_goal, 'savings': total})


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
    paginate_by = 2

    def get_queryset(self):
        return Category.objects.filter(user_id=self.request.session['id']).order_by('-name')

    def get_context_data(self, **kwargs):
        db = DB()
        total = float(db.savings_per_user(self.request.session['id']))

        context = super(CategoryIndexView, self).get_context_data(**kwargs)
        context['savings'] = total
        return context


# Show Income - Expense for each User[ID]
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'mycash/detail.html'


# Create Object Income to Save in DataBase
# The form 'IncomeForm' is displayed to enter the income data,
# when we send the form, if the form is valid, it saves the income data
# for the corresponding user and redirects to the overview page
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
            return redirect('mycash:income')

        return render(request, self.template_name, {'form': form})


# Create Object Income to Update in DataBase
class IncomeUpdate(UpdateView):
    model = Income
    form_class = IncomeUpdateForm
    template_name = 'mycash/manage-income.html'

    def get_success_url(self):
        return reverse('mycash:income')


class IncomeDelete(DeleteView):
    model = Income
    success_url = reverse_lazy('mycash:income')


# Create Object Expense to Save in DataBase
# When we go to the 'mycash/manage-expense.html' page,
# it shows us the form 'ExpenseForm'. If we filled it and send
# it, then the values sended will be validated and if it is ok,
# the expense data will be saved in the database
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
            return redirect('mycash:expense')

        return render(request, self.template_name, {'form': form})


# Create Object Income to Update in DataBase
class ExpenseUpdate(UpdateView):
    model = Expense
    form_class = ExpenseUpdateForm
    template_name = 'mycash/manage-expense.html'

    def get_success_url(self):
        return reverse('mycash:expense')


class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy('mycash:expense')


# Create Object Category to Save in DataBase
# If we go to the page 'mycash/manage-category.html',
# There will be the form 'CategoryForm' to fill the data of the new category,
# if the form is valid and the category didn't exist,
# it will save the new category in the database.
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
            cnt = Category.objects.filter(user_id=request.user.id, name=category.name).count()

            if cnt == 0:
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


class ExpenseIndexView(generic.ListView):
    template_name = "mycash/expense.html"
    context_object_name = 'all_expense'
    paginate_by = 6

    def get_queryset(self):
        qname = self.request.GET.get("name")
        qdate = self.request.GET.get("date")
        us_id = self.request.session['id']
        if qname and qdate:
            return Expense.objects.filter(
                Q(name__icontains=qname),
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('name')
        elif qname:
            return Expense.objects.filter(
                Q(name__icontains=qname),
                user_id=us_id,
            ).order_by('-date')

        elif qdate:
            return Expense.objects.filter(
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('name')

        return Expense.objects.filter(user_id=us_id).order_by('-date')

    def get_context_data(self, **kwargs):
        us_id = self.request.session['id']
        context = super(ExpenseIndexView, self).get_context_data(**kwargs)
        context['texpense'] = Expense.objects.filter(user_id=us_id).aggregate(Sum('amount'))
        return context


# List All Category for each User   [ID]
class IncomeIndexView(generic.ListView):
    template_name = 'mycash/income.html'
    context_object_name = 'all_income'
    paginate_by = 6

    def get_queryset(self):
        qname = self.request.GET.get("name")
        qdate = self.request.GET.get("date")
        us_id = self.request.session['id']
        if qname and qdate:
            return Income.objects.filter(
                Q(name__icontains=qname),
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('name')
        elif qname:
            return Income.objects.filter(
                Q(name__icontains=qname),
                user_id=us_id,
            ).order_by('-date')

        elif qdate:
            return Income.objects.filter(
                Q(date__icontains=qdate),
                user_id=us_id,
            ).order_by('name')

        return Income.objects.filter(user_id=us_id).order_by('-date')

    def get_context_data(self, **kwargs):
        us_id = self.request.session['id']
        context = super(IncomeIndexView, self).get_context_data(**kwargs)
        context['tincome'] = Income.objects.filter(user_id=us_id).aggregate(Sum('amount'))
        return context


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        us_id = self.request.session['id']
        all_income = Income.objects.filter(user_id=us_id).order_by('-date')
        all_expense = Expense.objects.filter(user_id=us_id).order_by('-date')
        user = MyUser.objects.get(pk=request.session['id'])
        db = DB()
        savings = float(db.savings_per_user(request.session['id']))

        context = {
            'all_income': all_income,
            'all_expense': all_expense,
            'user': user,
            'date': datetime.now(),
            'savings': savings,
        }

        pdf = render_to_pdf('mycash/report.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "report.pdf"
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


# Class ChartData to see Default Data Chart
# Data chart based on the days of week, it shows the expenses
# and incomes entered.
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        id_us = request.session['id']
        income_label = []
        expense_label = []
        income_amount = []
        expense_amount = []

        nd = 7
        nm = 7

        db = DB()

        # Data per day on income and expenses to be visualized visually
        incomes = db.income_month(id_us, nm)
        expenses = db.expense_day(id_us, nd)
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


# Class ChartView only use to redirect and see Charts
class ChartView(View):
    def get(self):
        return render(self.request, 'mycash/chart.html')


class HistoricalData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        # month = int(request.GET.get('search_month'))+1
        # year = request.GET.get('search_year')
        month = '7'
        year = '2018'
        id_us = request.session['id']

        days = Expense.objects.filter(user_id=id_us, date__year=year, date__month=month).annotate(day=Day('date')).values('day')\
            .annotate(amount=Sum('amount'))

        data = {"days": days}
        return Response(data)


# Class BudgetView only use to redirect and see Budget
class HistoricalView(View):
    def get(self, request):
        return render(request, 'mycash/historical.html')