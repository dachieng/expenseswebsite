from django.urls import path
from authentication import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('validate/', views.validate_username, name="validate"),
    path('validate-email/', views.validate_email_view, name="email-validate")
]
