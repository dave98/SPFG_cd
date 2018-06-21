from django.conf.urls import url
from . import views

# All url that system use in this Web Page
app_name = 'mycash'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),                                        # /mycash/
    url(r'^sign-in/', views.SignInView.as_view(), name='sign-in'),                               # /mycash/sign_in/
    url(r'^sign-up/', views.SignUpView.as_view(), name='sign-up'),                              # /mycash/sign_up/
    url(r'^log-out/', views.LogOutView.as_view(), name='log-out'),
    url(r'^del-account/', views.MyUserDeleteView.as_view(), name='del-account'),
    url(r'^profile/', views.ProfileView.as_view(), name='profile'),                             # /mycash/profile/
    url(r'^profile-edit/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name='profile-edit'),    # /mycash/profile-edit
    url(r'^overview/', views.CategoryIndexView.as_view(), name='overview'),                     # /mycash/overview/
    url(r'^detail/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(), name='detail'),        # /mycash/income/<pk>/

    url(r'^add-income/', views.IncomeCreate.as_view(), name='add-income'),                      # /mycash/add_income/
    url(r'^upd-income/(?P<pk>\d+)/$', views.IncomeUpdate.as_view(), name='upd-income'),         # /mycash/upd_income/
    url(r'^del-income/(?P<pk>\d+)/$', views.IncomeDelete.as_view(), name='del-income'),         # /mycash/upd_expense/

    url(r'^add-expense/', views.ExpenseCreate.as_view(), name='add-expense'),                   # /mycash/add_expense/
    url(r'^upd-expense/(?P<pk>\d+)/$', views.ExpenseUpdate.as_view(), name='upd-expense'),      # /mycash/upd_expense/
    url(r'^del-expense/(?P<pk>\d+)/$', views.ExpenseDelete.as_view(), name='del-expense'),      # /mycash/del_expense/

    url(r'^add-category/', views.CategoryCreate.as_view(), name='add-category'),                    # /mycash/add_category/
    url(r'^upd-category/(?P<pk>[0-9]+)/$', views.CategoryUpdate.as_view(), name='upd-category'),    # /mycash/uod_category/
    url(r'^del-category/(?P<pk>[0-9]+)/$', views.CategoryDelete.as_view(), name='del-category'),    # /mycash/del_category/

    url(r'^send-technical/', views.TechnicalRequestCreate.as_view(), name='send-technical'),                # /mycash/send-technical/

    # url(r'^goal/', views.GoalIndexView.as_view(), name='goal'),                         # /mycash/goal
    url(r'^goal/', views.GoalView.as_view(), name='goal'),                              # /mycash/goal
    url(r'^add-goal/', views.GoalCreate.as_view(), name='add-goal'),                    # /mycash/add_goal/
    url(r'^upd-goal/(?P<pk>[0-9]+)/$', views.GoalUpdate.as_view(), name='upd-goal'),    # /mycash/uod_goal/
    url(r'^del-goal/(?P<pk>[0-9]+)/$', views.GoalDelete.as_view(), name='del-goal'),    # /mycash/del_delete/

    url(r'^expense/', views.ExpenseIndexView.as_view(), name='expense'),                # /mycash/expense/
    url(r'^income/', views.IncomeIndexView.as_view(), name='income'),                   # /mycash/income/

    url(r'^chart/', views.ChartView.as_view(), name='chart'),                            # /mycash/chart/
    url(r'^api/chart/data', views.ChartData.as_view(), name='chart-data'),               # /mycash/api/chart/data/
]