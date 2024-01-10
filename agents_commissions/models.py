from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,AbstractUser,Group, 
Permission,PermissionsMixin)
import datetime


# Create your models here.

#For MainSite (Al-Nafi) User:
class Daily_lead(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length = 101, null=True, blank=True)
    product = models.CharField(max_length = 101, null=True, blank=True)
    amount = models.CharField(max_length = 101, null=True, blank=True)
    lead_creator = models.CharField(max_length =101, null=True, blank=True)
    al_baseer_verify = models.CharField(max_length =50, null=True, blank=True)
    crm_verify = models.CharField(max_length =50, null=True, blank=True)
    created_at = models.CharField(max_length =50, null=True, blank=True)

    def __str__(self):
        return f"{self.email}"