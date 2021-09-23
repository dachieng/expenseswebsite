from django.shortcuts import render


def register(request):
    return render(request, "authentication/register.html")
