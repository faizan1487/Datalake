from django.db import models
from user.models import User

class Expense(models.Model):
    subject = models.CharField(max_length=200,null=True,blank=True)
    amount = models.DecimalField(max_digits=55, decimal_places=2,null=True,blank=True)
    currency = models.CharField(max_length=10,null=True,blank=True)  # Assuming 3-letter currency code (e.g., USD, EUR)
    created_at = models.DateTimeField(auto_now_add=True)
    month = models.CharField(max_length=20,null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
 
    def __str__(self):
        return f"{self.subject}"

  