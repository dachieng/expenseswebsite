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

# Create your views here.


class IncomeListView(ListView, LoginRequiredMixin):
    model = UserIncome
    template_name = "incomes/incomes.html"
    context_object_name = "income"
    paginate_by = 2


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
