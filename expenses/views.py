from django.shortcuts import render


def home(request):
    return render(request, 'expenses/home.html')


def add_expenses(request):
    return render(request, 'expenses/add_expenses.html')
