from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.


def income(request):
    return HttpResponse("Hello")
