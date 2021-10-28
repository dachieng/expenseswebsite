from django.contrib import messages
from django.contrib.auth.models import User
from django.core import paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from expenses.forms import CreateExpense, ExpenseUpdateForm
from django.contrib.auth.decorators import login_required
from expenses.models import Expense, Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from userpreferences.models import UserPreference
import csv


@login_required
def home(request):
    expense = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expense, 2)
    currency = UserPreference.objects.get(user=request.user).currency
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'expenses/home.html', {'expense': expense, 'page_obj': page_obj, "currency": currency})


@login_required
def add_expenses(request):
    if request.method == "POST":
        form = CreateExpense(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.instance.owner = request.user
            form.save()
            messages.success(request, "expense created successfuly")

            return redirect("home")
    else:
        form = CreateExpense()
    return render(request, 'expenses/add_expenses.html', {'form': form})


@login_required
def detail_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expenses/detail_expense.html', {'expense': expense})


@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseUpdateForm(
            request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save(commit=False)
            form.instance.owner = request.user
            form.save()
            messages.success(request, "expense updated successfuly")
            return redirect("home")
    else:
        form = ExpenseUpdateForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', {'form': form, 'expense': expense})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense Removed")
        return redirect("home")
    return render(request, "expenses/expense_delete.html", {"expense": expense})


@csrf_exempt
def search_expense(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")
        expenses = Expense.objects.filter(amount__icontains=search_string, owner=request.user) | Expense.objects.filter(date__icontains=search_string, owner=request.user) | Expense.objects.filter(
            description__icontains=search_string, owner=request.user) | Expense.objects.filter(category__icontains=search_string, owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


def export_csv_expenses(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="expenses.csv"'},)

    writer = csv.writer(response)

    writer.writerow(['Amount', 'Date', 'Description', 'Category'])

    expenses = Expense.objects.filter(owner=request.user)

    for e in expenses:
        writer.writerow([e.amount, e.date, e.description, e.category])
    return response
