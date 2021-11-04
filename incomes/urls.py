from incomes import views
from django.urls import path

urlpatterns = [
    path("", views.IncomeListView.as_view(), name="income"),
    path("details/<int:pk>/", views.IncomeDetailListView.as_view(),
         name="income-detail"),

    path("add-income/", views.IncomeCreateView.as_view(), name="add-income"),
    path("update-income/<int:pk>/",
         views.UserIncomeUpdateView.as_view(), name="update-income"),

    path("delete-income/<int:pk>/",
         views.UserIncomeDeleteView.as_view(), name="delete-income"),

    path("search-income/", views.search_income, name="search-income"),
    path("export-csv-incomes/", views.export_csv_incomes,
         name="export-csv-incomes"),
    path('income-summary/', views.incomes_summary, name="income-summary"),
    path('income-stats/', views.income_stats, name="income-stats")
]
