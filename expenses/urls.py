from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('index', views.index, name="index"),
    path('register', views.register_page, name="register_page"),
    path('register_new', views.register_new, name="register_new"),
    path('success', views.success, name="success"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('account_page', views.account_page, name="account_page"),
    path('add_expense_category', views.add_expense_category,
         name="add_expense_category"),
    path('add_income_category', views.add_income_category,
         name="add_income_category"),
    path('delete_expense_category', views.delete_expense_category,
         name="delete_expense_category"),
    path('delete_income_category', views.delete_income_category,
         name="delete_income_category"),

    path('add_expense', views.add_expense, name="add_expense"),
    path('add_expense_item', views.add_expense_item, name="add_expense_item"),
    path('edit_expense/<int:id>', views.edit_expense, name="edit_expense"),
    path('update_expense/<int:id>', views.update_expense, name="update_expense"),
    path('delete_expense/<int:id>', views.delete_expense, name="delete_expense"),

    path('add_income', views.add_income, name="add_income"),
    path('add_income_item', views.add_income_item, name="add_income_item"),
    path('edit_income/<int:id>', views.edit_income, name="edit_income"),
    path('update_income/<int:id>', views.update_income, name="update_income"),
    path('delete_income/<int:id>', views.delete_income, name="delete_income"),

    path('expense_summary', views.expense_summary, name="expense_summary"),
    path('income_summary', views.income_summary, name="income_summary"),
    path('expense_monthly_chart', views.expense_monthly_chart,
         name="expense_monthly_chart"),
    path('income_monthly_chart', views.income_monthly_chart,
         name="income_monthly_chart"),

    path('search_expenses', csrf_exempt(
        views.search_expenses), name="search_expenses"),
    path('search_incomes', csrf_exempt(
        views.search_incomes), name="search_incomes"),


]
