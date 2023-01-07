from django.db import models

# Create your models here.

class Payment(models.Model):
    payment_source = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    enrollment_name = models.CharField(max_length=50)
    enrollment_creation_date = models.DateTimeField(auto_now_add=True)
    enrollment_expiry_date = models.DateTimeField()
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email