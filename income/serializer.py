from django.db import models
from django.db.models import fields
from .models import Income
from rest_framework import serializers

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['source','amount','description']