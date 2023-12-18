from django.db import models
from user.models import User

class Expense(models.Model):
    subject = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=65, decimal_places=2)
    currency = models.CharField(max_length=10)  # Assuming 3-letter currency code (e.g., USD, EUR)
    created_at = models.DateTimeField(auto_now_add=True)
    month = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
 
    def __str__(self):
        return f"{self.subject}"

  