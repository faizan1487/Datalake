from django.db import models

# Create your models here.

class Payment(models.Model):
    payment_source = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    enrollment_name = models.CharField(max_length=50)
    enrollment_creation_date = models.CharField(max_length=80,null=True,blank=True)
    enrollment_expiry_date = models.CharField(max_length=80,null=True,blank=True)
    payment_date = models.CharField(max_length=80,null=True,blank=True)

    def __str__(self):
        return self.email