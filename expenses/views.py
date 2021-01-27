from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Expense, Income, ExpenseCategory, IncomeCategory
import bcrypt
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import datetime
from django.views.generic import ListView
# Create your views here.


def index(request):
    return redirect('success')


def register_page(request):
    return render(request, 'register.html')


def login_page(request):
    return render(request, 'login.html')


def register_new(request):
    if request.method == "POST":
        errors = User.objects.basic_validation(request.POST)
        if User.objects.filter(email=request.POST['email']):
            messages.error(request, 'email is already used')
            return redirect('/register')
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(
                password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            new_user = User.objects.create(
                name=request.POST['name'],
                email=request.POST['email'],
                password=pw_hash)
            request.session['userid'] = new_user.id
            return redirect('/success')
    return redirect('/register')


def success(request):
    if 'userid' in request.session:
        user = User.objects.filter(id=request.session['userid'])
        if user:
            context = {
                'user': user[0]
            }
            return render(request, 'success.html', context)
    return redirect('/')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                return redirect('/success')
            else:
                messages.error(request, "Password Incorrect")
                return redirect('/')
        else:
            messages.error(request, "Please enter an valid email address")
            return redirect('/')
    return redirect('/')


def logout(request):
    if request.session['userid']:
        print('logging out')
        request.session['userid'] = None
    return redirect('/')


def expense_summary(request):
    current_user = User.objects.get(id=request.session['userid'])
    expenses = Expense.objects.filter(owner=current_user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'expenses': expenses,
        'current_user': current_user,
        'page_obj': page_obj
    }
    return render(request, 'expense_summary.html', context)


def income_summary(request):
    current_user = User.objects.get(id=request.session['userid'])
    incomes = Income.objects.filter(owner=current_user)
    paginator = Paginator(incomes, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'incomes': incomes,
        'current_user': current_user,
        'page_obj': page_obj
    }
    return render(request, 'income_summary.html', context)


def add_expense(request):
    user = User.objects.get(id=request.session['userid'])
    expense_category_name = ExpenseCategory.objects.filter(owner=user)
    context = {
        'values': request.POST,
        'expense_category_name': expense_category_name
    }
    return render(request, 'add_expense.html', context)


def add_expense_item(request):
    if request.method == "POST":
        errors = Expense.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_expense')
        else:
            Expense.objects.create(
                amount=request.POST['amount'],
                date=request.POST['expense_date'],
                description=request.POST['description'],
                owner=User.objects.get(id=request.session['userid']),
                category=request.POST['category']
            )
            return redirect('expense_summary')
    return redirect('/add_expense')


def edit_expense(request, id):
    if request.method == "GET":
        user = User.objects.get(id=request.session['userid'])
        expense_category_name = ExpenseCategory.objects.filter(owner=user)
        values = Expense.objects.get(id=id)
        context = {
            'values': values,
            'expense_category_name': expense_category_name
        }
        return render(request, 'edit_expense.html', context)


def update_expense(request, id):
    current_user = User.objects.get(id=request.session['userid'])
    values = Expense.objects.get(id=id)
    context = {
        'values': values
    }
    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount Required')
            return render(request, 'edit_expense.html', context)

        date = request.POST['expense_date']
        category = request.POST['category']
        description = request.POST['description']

        if not description:
            messages.error(request, 'Description Required')
            return render(request, 'edit_expense.html', context)

        values.owner = current_user
        values.amount = amount
        values.date = date
        values.category = category
        values.description = description
        values.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('expense_summary')


def add_income(request):
    user = User.objects.get(id=request.session['userid'])
    income_category_name = IncomeCategory.objects.filter(owner=user)
    context = {
        'values': request.POST,
        'income_category_name': income_category_name
    }
    return render(request, 'add_income.html', context)


def update_income(request, id):
    current_user = User.objects.get(id=request.session['userid'])
    values = Income.objects.get(id=id)
    context = {
        'values': values
    }
    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount Required')
            return render(request, 'edit_income.html', context)

        date = request.POST['income_date']
        category = request.POST['category']
        description = request.POST['description']

        if not description:
            messages.error(request, 'Description Required')
            return render(request, 'edit_income.html', context)

        values.owner = current_user
        values.amount = amount
        values.date = date
        values.category = category
        values.description = description
        values.save()
        messages.success(request, 'Income updated successfully')

        return redirect('income_summary')


def add_income_item(request):
    if request.method == "POST":
        errors = Income.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_income')
        else:
            Income.objects.create(
                amount=request.POST['amount'],
                date=request.POST['income_date'],
                description=request.POST['description'],
                owner=User.objects.get(id=request.session['userid']),
                category=request.POST['category']
            )
            return redirect('income_summary')
    return redirect('/add_income')


def edit_income(request, id):
    if request.method == "GET":
        user = User.objects.get(id=request.session['userid'])
        income_category_name = IncomeCategory.objects.filter(owner=user)
        values = Income.objects.get(id=id)
        context = {
            'values': values,
            'income_category_name': income_category_name
        }
        return render(request, 'edit_income.html', context)


def expense_monthly_chart(request):
    today_date = datetime.date.today()
    six_months_ago = today_date-datetime.timedelta(days=30*6)
    user = User.objects.get(id=request.session['userid'])
    expenses = Expense.objects.filter(owner=user,
                                      date__gte=six_months_ago, date__lte=today_date)
    finalrep = {}
    labels = []
    data = []

    def get_month(expense):
        return expense.date.month
    month_list = list(set(map(get_month, expenses)))

    def get_expense_month_amount(month):
        amount = 0
        filter_by_month = expenses.filter(date__month=month)

        for item in filter_by_month:
            amount += item.amount
        return amount

    for x in expenses:
        for y in month_list:
            finalrep[y] = get_expense_month_amount(y)

    labels = list(finalrep.keys())
    data = list(finalrep.values())

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def income_monthly_chart(request):
    today_date = datetime.date.today()
    six_months_ago = today_date-datetime.timedelta(days=30*6)
    user = User.objects.get(id=request.session['userid'])
    incomes = Income.objects.filter(owner=user,
                                    date__gte=six_months_ago, date__lte=today_date)
    finalrep = {}
    labels = []
    data = []

    def get_month(income):
        return income.date.month
    month_list = list(set(map(get_month, incomes)))

    def get_income_month_amount(month):
        amount = 0
        filter_by_month = incomes.filter(date__month=month)

        for item in filter_by_month:
            amount += item.amount
        return amount

    for x in incomes:
        for y in month_list:
            finalrep[y] = get_income_month_amount(y)

    labels = list(finalrep.keys())
    data = list(finalrep.values())

    return JsonResponse({'income_category_data': finalrep}, safe=False)


def delete_expense(request, id):
    expense = Expense.objects.get(id=id)
    expense.delete()
    messages.info(request, 'Expense Deleted')
    return redirect('expense_summary')


def delete_income(request, id):
    income = Income.objects.get(id=id)
    income.delete()
    messages.info(request, 'Income Deleted')
    return redirect('income_summary')


def test_page(request):
    return render(request, 'test.html')


def search_expenses(request):
    current_user = User.objects.get(id=request.session['userid'])
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=current_user) | Expense.objects.filter(
            date__istartswith=search_str, owner=current_user) | Expense.objects.filter(
            description__icontains=search_str, owner=current_user) | Expense.objects.filter(
            category__icontains=search_str, owner=current_user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


def search_incomes(request):
    current_user = User.objects.get(id=request.session['userid'])
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        incomes = Income.objects.filter(
            amount__istartswith=search_str, owner=current_user) | Income.objects.filter(
            date__istartswith=search_str, owner=current_user) | Income.objects.filter(
            description__icontains=search_str, owner=current_user) | Income.objects.filter(
            category__icontains=search_str, owner=current_user)
        data = incomes.values()
        return JsonResponse(list(data), safe=False)


def account_page(request):
    if 'userid' in request.session:
        user = User.objects.get(id=request.session['userid'])
        expense_category_name = ExpenseCategory.objects.filter(owner=user)
        income_category_name = IncomeCategory.objects.filter(owner=user)
        if user:
            context = {
                'user': user,
                'expense_category_name': expense_category_name,
                'income_category_name': income_category_name
            }
            return render(request, "account.html", context)
    return redirect('/')


def add_expense_category(request):
    if request.method == "POST":
        current_user = User.objects.get(id=request.session['userid'])
        errors = ExpenseCategory.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/account_page')
        else:
            ExpenseCategory.objects.create(
                name=request.POST['category_name'],
                owner=current_user
            )
            messages.success(request, 'Category added successfully')
            return redirect('/account_page')
    return redirect('/account_page')


def add_income_category(request):
    if request.method == "POST":
        current_user = User.objects.get(id=request.session['userid'])
        errors = IncomeCategory.objects.basic_validation(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/account_page')
        else:
            IncomeCategory.objects.create(
                name=request.POST['category_name'],
                owner=current_user
            )
            messages.success(request, 'Category added successfully')
            return redirect('/account_page')
    return redirect('/account_page')


def delete_expense_category(request):
    expense_category = ExpenseCategory.objects.get(
        name=request.POST['category'])
    expense_category.delete()
    messages.info(request, 'Category Deleted')
    return redirect('account_page')


def delete_income_category(request):
    income_category = IncomeCategory.objects.get(
        name=request.POST['category'])
    income_category.delete()
    messages.info(request, 'Category Deleted')
    return redirect('account_page')
