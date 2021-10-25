from incomes import views
from django.urls import path

urlpatterns = [
    path("", views.income, name="income")
]
