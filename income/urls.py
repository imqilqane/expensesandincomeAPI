from django.urls import path
from . import views
urlpatterns = [
    path('', views.IncomesListAPIView.as_view(), name='incomes'),    
    path('<str:id>/', views.incomeGetAPIView.as_view(), name='income'),    
]
