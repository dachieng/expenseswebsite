from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.home, name="home"),
    path('add_expenses/', views.add_expenses, name="")

]
