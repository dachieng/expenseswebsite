from django.urls import path
from authentication import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('validate/', views.validate_username, name="validate"),
    path('validate-email/', views.validate_email_view, name="email-validate"),
    path('activate-account/<uidb64>/<token>/',
         views.activate_account, name="activate-account"),
    path("login/", auth_views.LoginView.as_view(template_name="authentication/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        template_name="authentication/logout.html"), name="logout")
]
