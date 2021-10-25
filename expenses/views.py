from django.contrib import messages
from django.core import paginator
from django.shortcuts import redirect, render
from expenses.forms import CreateExpense, ExpenseUpdateForm
from django.contrib.auth.decorators import login_required
from expenses.models import Expense, Category
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json
from django.http import JsonResponse


@login_required
def home(request):
    expense = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expense, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    return render(request, 'expenses/home.html', {'expense': expense, 'page_obj': page_obj})


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
    category = Category.objects.all()
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
    return render(request, 'expenses/edit_expense.html', {'form': form})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    messages.success(request, "Expense Removed")
    return redirect("home")


"""def search_expense(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")
        expenses = Expense.objects.filter(amount__starts_with=search_string, owner=request.user) | Expense.objects.filter(date__starts_with=search_string, owner=request.user) | Expense.objects.filter(
            description__starts_with=search_string, owner=request.user) | Expense.objects.filter(category__starts_with=search_string, owner=request.user)

        data = """
