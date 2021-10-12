from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from authentication.forms import UserRegistrationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f" {username}, your account has been created successfully")
            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(request, "authentication/register.html", {'form': form})


@csrf_exempt
def validate_username(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({"username_error": "Username should contain only alphanumeric characters"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_exists': 'Username already Taken'}, status=409)

        return JsonResponse({"username_valid": True})
