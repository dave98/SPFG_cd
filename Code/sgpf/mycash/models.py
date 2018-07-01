from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, RegexValidator
from django.core.urlresolvers import reverse
from datetime import datetime
from django.utils import timezone
from django.db import models

"""
    Mapping of the classes described below, all these are converted into tables 
    in the database, and in case complementary tables can be created for relationships 
    that have.
"""


# class controller MyUser create
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


# MyUser class [User]
class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=50, unique=True)  # user email
    nickname = models.CharField(max_length=20, validators=[
        RegexValidator(regex='^[\w\s]*$', message='Nickname must be Alphanumeric', code='invalid_nickname')])

    name = models.CharField(max_length=30, validators=[
        RegexValidator(regex='^[a-zA-Z\s]*$', message='Name must be Alphabetic', code='invalid_name')])

    last_name = models.CharField(max_length=50, validators=[
        RegexValidator(regex='^[a-zA-Z\s]*$', message='Name must be Alphabetic', code='invalid_last_name')])

    phone = models.CharField(max_length=12, validators=[
        RegexValidator(regex='^[0-9]*$', message='Nickname must be Numeric', code='invalid_phone')])        # user phone

    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile', blank=True, default='profile/user.png')
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
    name = models.CharField(max_length=30, validators=[
        RegexValidator(regex='^[a-zA-Z]*$', message='Name must be Alphabetic', code='invalid_name')])
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    create_on = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('mycash:detail', kwargs={'pk': self.pk})

    @classmethod
    def create(cls, name, user):
        category = cls(name=name, user=user)
        return category

    def __str__(self):
        return self.name


# Income class that will be mapped in the database as a table. [mycash_income]
class Income(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.001)])
    name = models.CharField(max_length=20, validators=[
        RegexValidator(regex='^[\w\s]*$', message='Name must be Alphanumeric', code='invalid_name'),
    ])
    date = models.DateField(default=datetime.now)

    def get_income(self):
        return self.recipephotos_set.filter(type="3")


# Expense class that will be mapped in the database as a table. [mycash_expense]
class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.001)])
    name = models.CharField(max_length=20, validators=[
        RegexValidator(regex='^[\w\s]*$', message='Name must be Alphanumeric', code='invalid_name'),
    ])
    date = models.DateField(default=datetime.now)


class TechnicalRequest(models.Model):
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    send_on = models.DateField(default=datetime.now)


# Goal class
class Goal(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, validators=[
        RegexValidator(regex='^[\w\s]*$', message='Name must be Alphanumeric', code='invalid_name'),
    ])
    percentage = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.00)])
    adv_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.001)])