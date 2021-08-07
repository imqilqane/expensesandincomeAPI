from django.urls import path
from . import views

urlpatterns = [
  path('', views.ExpensesListAPIView.as_view(), name="expenses"),
  path('<str:id>/', views.ExpenseAPIView.as_view(), name="expense")
]
