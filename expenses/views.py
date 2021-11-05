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
import datetime
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum


@login_required
def home(request):
    expense = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expense, 4)
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


def expense_summary(request):
    today = datetime.date.today()
    one_month_ago = today - datetime.timedelta(days=30)  # 1 week ago

    # gte = greater than
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=one_month_ago, date__lte=today)

    # return key value pair for category and the total amount
    category_set = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0

        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for x in expenses:
        for y in category_list:
            category_set[y] = get_expense_category_amount(y)

    return JsonResponse({"expense_category_data": category_set}, safe=False)


def expense_stats(request):
    return render(request, "expenses/expenses_stats.html")


def export_excel_expenses(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="expense_summary.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Incomes Summary')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Date', 'Description', 'Category']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list(
        'amount', 'date', 'description', 'category')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_pdf_expenses(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename="expenses.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'

    expenses = Expense.objects.filter(owner=request.user)

    sum = expenses.aggregate(Sum('amount'))

    html_string = render_to_string(
        "expenses/expenses_pdf.html", {'expenses': expenses, 'total': sum['amount__sum']})

    html = HTML(string=html_string)

    result = html.write_pdf()

    # preview the pdf in memory before printing it
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)

        output.flush()

        output = open(output.name, 'rb')

        response.write(output.read())

    return response
