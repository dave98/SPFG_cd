from django.contrib import admin
from .models import User, UserType, Category, Income, Expense

# Register your models here.


# Class to see User Type in the admin site.
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'photo')


# Class to see User in the admin site.
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_name', 'email', 'phone', 'state')


# Class to see Category in the admin site
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create')


# Class to see Income in the admin site
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


admin.site.register(UserType, UserTypeAdmin)    # admin create user-type.
admin.site.register(User, UserAdmin)            # admin create user.
admin.site.register(Category, CategoryAdmin)    # admin create category.
admin.site.register(Income, IncomeAdmin)        # admin create income.
admin.site.register(Expense, ExpenseAdmin)      # admin create income.
# maldonado - verschrankung
