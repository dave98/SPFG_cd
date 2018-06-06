from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models

"""
    Mapping of the classes described below, all these are converted into tables 
    in the database, and in case complementary tables can be created for relationships 
    that have.
"""


class PerBaseUserManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, unique=True)  # user email
    nickname = models.CharField(max_length=20)
    name = models.CharField(max_length=30)  # user name
    last_name = models.CharField(max_length=50)  # user last name
    phone = models.CharField(max_length=12)  # user phone optional
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = PerBaseUserManager()

    def get_full_name(self):
        cad = "{0} {1}"
        return cad.format(self.name, self.last_name)

    def get_short_name(self):
        return self.nickname

    def __str__(self):  # print
        cad = "{0} {1}, {2}"
        return cad.format(self.name, self.last_name, self.email)


# Category class that will be mapped in the database as a table. [mycash_category]
class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('mycash:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


# Income class that will be mapped in the database as a table. [mycash_income]
class Income(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=20)
    date = models.DateField()


# Expense class that will be mapped in the database as a table. [mycash_expense]
class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=20)
    date = models.DateField()