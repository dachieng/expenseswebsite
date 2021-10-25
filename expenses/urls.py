from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.home, name="home"),
    path('search_expense/', views.search_expense, name="search_expense"),
    path('add_expenses/', views.add_expenses, name="add-expenses"),
    path('edit_expense/<int:pk>/', views.update_expense, name="edit-expense"),
    path('expense_detail/<int:pk>/', views.detail_expense, name="detail-expense"),
    path('expense_delete/<int:pk>/', views.delete_expense, name="delete-expense"),
]
