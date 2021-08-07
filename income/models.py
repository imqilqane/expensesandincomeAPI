from django.db import models
from mainApp.models import User

class Income(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self) :
        return self.owner.username
