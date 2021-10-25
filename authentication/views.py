from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from authentication.forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from validate_email import validate_email
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
from authentication.utils import token_generator

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode  # uidb64
# get the domain of our current site
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get("username")
            to_email = form.cleaned_data.get("email")
            from_email = settings.EMAIL_HOST_USER
            subject = "Activate Your Account"
            message = f"{username} please use this link to activate your account"

            # send email configurations
            # get the domain
            domain = get_current_site(request).domain

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # get the relative url of the activate view

            link = reverse(
                'activate-account', kwargs={"uidb64": uidb64, "token": token_generator.make_token(user)})

            activate_url = "http://"+domain+link

            to_email = form.cleaned_data.get("email")
            from_email = settings.EMAIL_HOST_USER
            subject = "Activate Your Account"
            message = f"{username} please use this link to activate your account {activate_url}"

            email_message = EmailMessage(
                subject,
                message,
                from_email,
                [to_email],
            )

            email_message.send(fail_silently=False)

            messages.success(
                request, f" {username}, your account has been created successfully. Check your email to activate account")
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


@csrf_exempt
def validate_email_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'invalid_email': "Enter a valid email"})
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_exists": "Email already Taken"})
        return JsonResponse({'email_valid': True})


# activate user account
@csrf_exempt
def activate_account(request, uidb64, token):
    if request.method == "GET":

        try:
            # get the uid
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect("login"+"?message"+"account is already active")

            if user.is_active:
                return redirect("login")
            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully")
            return redirect("login")
        except Exception as e:
            pass

        return redirect("home")


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(
            request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "profile updated successfully")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "authentication/profile.html", {"u_form": u_form, "p_form": p_form})
