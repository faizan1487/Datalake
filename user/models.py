from django.db import models

# Create your models here.

#For User:
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=50, default="PK")
    created_at= models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.username
