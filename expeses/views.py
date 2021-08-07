from django.shortcuts import render
from .serializers import ExpenseSerializer
from .models import Expense
from .permissions import IsOwner
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .pagination import PostLimitOfPage


class ExpensesListAPIView(ListCreateAPIView):

    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = PostLimitOfPage

    # ovverid this func to bind the created expense with it onwner
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    # ovverid this func to show the user just is own expenses
    def get_queryset(self): 
        return self.queryset.filter(owner = self.request.user)


class ExpenseAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
    
    # ovverid this func to show the user just is own expenses
    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)