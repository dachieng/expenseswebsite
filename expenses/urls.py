from django.urls import path
from expenses import views


urlpatterns = [
    path('', views.home, name="home"),
    path('search_expense/', views.search_expense, name="search_expense"),
    path('add_expenses/', views.add_expenses, name="add-expenses"),
    path('edit_expense/<int:pk>/', views.update_expense, name="edit-expense"),
    path('expense_detail/<int:pk>/', views.detail_expense, name="detail-expense"),
    path('expense_delete/<int:pk>/', views.delete_expense, name="delete-expense"),
    path('export-csv-expenses/', views.export_csv_expenses,
         name="export-csv-expenses"),
    path('expense-summary/', views.expense_summary, name="expense-summary"),
    path('expense-stats/', views.expense_stats, name="expense-stats"),
    path('export_excel_expenses/', views.export_excel_expenses,
         name="export_excel_expenses"),
    path('export_pdf_expenses', views.export_pdf_expenses,
         name="export_pdf_expenses")
]
