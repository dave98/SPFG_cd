from django.conf.urls import url
from . import views

# All url that system use in this Web Page
app_name = 'mycash'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),                                        # /mycash/
    url(r'^sign_in/', views.LoginView.as_view(), name='sign-in'),                               # /mycash/sign_in/
    url(r'^sign_up/', views.UserCreate.as_view(), name='sign-up'),                              # /mycash/sign_up/
    url(r'^profile/', views.ProfileView.as_view(), name='profile'),                             # /mycash/profile/
    url(r'^profile-edit/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name='profile-edit'),    # /mycash/profile-edit
    url(r'^overview/', views.CategoryIndexView.as_view(), name='overview'),                     # /mycash/overview/
    url(r'^income/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(), name='detail'),        # /mycash/income/<pk>/
    url(r'^budget/', views.BudgetView.as_view(), name='budget'),                                # /mycash/budget/
    url(r'^add_income/', views.IncomeCreate.as_view(), name='add_income'),                      # /mycash/add_income/
    url(r'^upd_income/(?P<pk>\d+)/$', views.IncomeUpdate.as_view(), name='upd_income'),         # /mycash/upd_income/
    url(r'^add_expense/', views.ExpenseCreate.as_view(), name='add_expense'),                   # /mycash/add_expense/
    url(r'^upd_expense/(?P<pk>\d+)/$', views.ExpenseUpdate.as_view(), name='upd_expense'),      # /mycash/upd_expense/
    url(r'^chart/', views.ChartView.as_view(), name='chart'),                                   # /mycash/chart/
    url(r'^api/chart/data', views.ChartData.as_view(), name='chart-data'),                      # /mycash/api/chart/data/
]