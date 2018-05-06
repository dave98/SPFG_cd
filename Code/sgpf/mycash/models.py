from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models


# UserType class that will be mapped in the database as a table. [mycash_usertype]
class UserType(models.Model):
    type = models.CharField(max_length=20)
    photo = models.CharField(max_length=500)

    def get_absolute_url(self):
        return reverse('mycash:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.type


# User class that will be mapped in the database as a table. [mycash_user]
class User(models.Model):
    user_type = models.ForeignKey(UserType, on_delete=models.CASCADE)   # fk to pk of user type
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=20)                              # user name
    last_name = models.CharField(max_length=50)                         # user last name
    email = models.CharField(max_length=50)                             # user email
    phone = models.CharField(max_length=12)                             # user phone optional
    state = models.BooleanField(default=True)                           # user state [delete]

    def __str__(self):                                                  # print
        cad = "{0} {1}, {2}"
        return cad.format(self.name, self.last_name, self.email)


# Category class that will be mapped in the database as a table. [mycash_category]
class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('mycash:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


# Income class that will be mapped in the database as a table. [mycash_income]
class Income(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)


# Expense class that will be mapped in the database as a table. [mycash_expense]
class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)