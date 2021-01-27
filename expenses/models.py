from django.db import models
import re
from django.utils.timezone import now

# Create your models here.


class UserManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors['name'] = 'Name should be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        if postData['password'] != postData['confirm_pw']:
            errors['pw'] = 'Password and Confirm Password do not match'
        return errors


class ExpenseManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['category']) == 0:
            errors['category'] = 'Please enter a category'
        if len(postData['amount']) == 0:
            errors['amount'] = 'Please enter an amount'
        if len(postData['expense_date']) == 0:
            errors['expense_date'] = 'Please enter an date'
        return errors


class IncomeManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['category']) == 0:
            errors['category'] = 'Please enter a category'
        if len(postData['amount']) == 0:
            errors['amount'] = 'Please enter an amount'
        if len(postData['income_date']) == 0:
            errors['income_date'] = 'Please enter an date'
        return errors


class CategoryManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        if len(postData['category_name']) == 0:
            errors['category_name'] = 'Please enter a category name'
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(
        User, related_name="expense_by_user", on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExpenseManager()

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']


class Income(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(
        User, related_name="income_by_user", on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = IncomeManager()

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name="expense_category_by_user", on_delete=models.CASCADE)
    objects = CategoryManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class IncomeCategory(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name="income_category_by_user", on_delete=models.CASCADE)
    objects = CategoryManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
