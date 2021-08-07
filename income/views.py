from django.shortcuts import render
from .serializer import IncomeSerializer
from rest_framework import generics
from .models import Income
from rest_framework.permissions import IsAuthenticated
from expeses.permissions import IsOwner

class IncomesListAPIView(generics.ListCreateAPIView):
    
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        return serializer.save(owner = self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)


class incomeGetAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner = self.request.user)
