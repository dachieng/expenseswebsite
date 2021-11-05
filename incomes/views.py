from django.http.response import HttpResponse
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from incomes.models import UserIncome
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from incomes.forms import UserIncomeCreationForm, UserIncomeUpdateForm
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
import json
from django.http.response import JsonResponse
import csv
import datetime
from django.shortcuts import render
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum


# Create your views here.


class IncomeListView(ListView, LoginRequiredMixin):
    model = UserIncome
    template_name = "incomes/incomes.html"
    context_object_name = "income"
    paginate_by = 4


class IncomeDetailListView(DetailView, LoginRequiredMixin):
    model = UserIncome
    template_name = "incomes/incomes_detail.html"
    context_object_name = "income"


class IncomeCreateView(CreateView, LoginRequiredMixin):
    model = UserIncome
    form_class = UserIncomeCreationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    # fields = ['amount', 'source', 'description', 'date']


class UserIncomeUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = UserIncome
    form_class = UserIncomeUpdateForm
    template_name = "incomes/income_update.html"
    context_object_name = "income"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        income = self.get_object()
        if self.request.user == income.owner:
            return True
        return False
    success_url = reverse_lazy("income")


class UserIncomeDeleteView(DeleteView, LoginRequiredMixin):
    model = UserIncome

    def test_func(self):
        income = self.get_object()
        if self.request.user == income.owner:
            return True
        return False
    success_url = reverse_lazy("income")


@csrf_exempt
def search_income(request):
    if request.method == "POST":
        search_string = json.loads(request.body).get("searchText")
        incomes = UserIncome.objects.filter(amount__icontains=search_string, owner=request.user) | UserIncome.objects.filter(date__icontains=search_string, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_string, owner=request.user) | UserIncome.objects.filter(source__icontains=search_string, owner=request.user)

        data = incomes.values()

        return JsonResponse(list(data), safe=False)


def export_csv_incomes(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="incomes.csv"'},)

    writer = csv.writer(response)

    writer.writerow(['Amount', 'Date', 'Description', 'Source'])

    incomes = UserIncome.objects.filter(owner=request.user)

    for i in incomes:
        writer.writerow([i.amount, i.date, i.description, i.source])
    return response


def incomes_summary(request):
    today = datetime.date.today()
    one_month_ago = today - datetime.timedelta(days=30)  # 1 week ago

    # gte = greater than
    incomes = UserIncome.objects.filter(owner=request.user,
                                        date__gte=one_month_ago, date__lte=today)

    # return key value pair for category and the total amount
    source_set = {}

    def get_source(income):
        return income.source

    source_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0

        filtered_by_source = incomes.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount

        return amount

    for x in incomes:
        for y in source_list:
            source_set[y] = get_income_source_amount(y)

    return JsonResponse({"income_source_data": source_set}, safe=False)


def income_stats(request):
    return render(request, "incomes/income_stats.html")


def export_excel_incomes(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="income_summary.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Incomes Summary')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Date', 'Description', 'Source']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = UserIncome.objects.filter(owner=request.user).values_list(
        'amount', 'date', 'description', 'source')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_pdf_incomes(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename="incomes.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'

    incomes = UserIncome.objects.filter(owner=request.user)

    sum = incomes.aggregate(Sum('amount'))

    html_string = render_to_string(
        "incomes/incomes_pdf.html", {'incomes': incomes, 'total': sum['amount__sum']})

    html = HTML(string=html_string)

    result = html.write_pdf()

    # preview the pdf in memory before printing it
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)

        output.flush()

        output = open(output.name, 'rb')

        response.write(output.read())

    return response
