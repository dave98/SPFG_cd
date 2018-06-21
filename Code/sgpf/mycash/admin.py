from django.contrib import admin
from .models import Category, Income, Expense, MyUser, TechnicalRequest, Goal
from django.contrib.auth.admin import UserAdmin

"""
    Administrator Panel, All our measures are displayed, and we can access it and add it by:
        https://localhost: 8000 / admin
"""


class MyUserAdmin(UserAdmin):
    fieldsets = ()
    add_fieldsets = (
        (None, {'fields', ('email', 'password1', 'password2'), })
    )
    list_display = ('email', 'nickname', 'name', 'is_active', 'is_staff',)
    search_fields = ('nickname', 'name')
    ordering = ('nickname',)


# Class to see Category in the admin site
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_on')


# Class to see Income in the admin site
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


class TechnicalRequestAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'state')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'amount', 'percentage')


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Goal, GoalAdmin)    # admin create category.
admin.site.register(Category, CategoryAdmin)    # admin create category.
admin.site.register(Income, IncomeAdmin)        # admin create income.
admin.site.register(Expense, ExpenseAdmin)      # admin create income.
admin.site.register(TechnicalRequest, TechnicalRequestAdmin)      # admin create income.