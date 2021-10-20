from userpreferences import views
from django.urls import path

urlpatterns = [
    path("", views.user_settings, name="user-settings")
]
