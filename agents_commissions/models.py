from enum import unique
from pyexpat import model
from django.db import models
from django.contrib.auth.models import (BaseUserManager,AbstractBaseUser,AbstractUser,Group, 
Permission,PermissionsMixin)
import datetime


# Create your models here.

class Daily_lead(models.Model):
    id = models.CharField(max_length=255, unique=True,primary_key=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length = 101, null=True, blank=True)
    product = models.CharField(max_length = 101, null=True, blank=True)
    plan = models.CharField(max_length = 101, null=True, blank=True)
    renewal = models.CharField(max_length = 101, null=True, blank=True)
    is_exam_fee = models.CharField(max_length = 101, null=True, blank=True)
    amount = models.CharField(max_length = 101, null=True, blank=True)
    source = models.CharField(max_length = 101, null=True, blank=True)
    lead_creator = models.CharField(max_length =101, null=True, blank=True)
    manager_approval = models.CharField(max_length =50, null=True, blank=True)
    manager_approval_crm = models.CharField(max_length =50, null=True, blank=True)
    veriification_cfo = models.CharField(max_length =50, null=True, blank=True)
    support = models.CharField(max_length =50, null=True, blank=True)
    completely_verified = models.CharField(max_length =50, null=True, blank=True)
    paid = models.CharField(max_length =50, null=True, blank=True)
    is_comission = models.BooleanField(default = False)
    created_at = models.CharField(max_length =50, null=True, blank=True)

    def __str__(self):
        return f"{self.email}"
    
class Daily_Sales_Support(models.Model):
    id = models.CharField(max_length=255, unique=True,primary_key=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length = 101, null=True, blank=True)
    product = models.CharField(max_length = 101, null=True, blank=True)
    plan = models.CharField(max_length = 101, null=True, blank=True)
    is_exam_fee = models.CharField(max_length = 101, null=True, blank=True)
    amount = models.CharField(max_length = 101, null=True, blank=True)
    source = models.CharField(max_length = 101, null=True, blank=True)
    lead_creator = models.CharField(max_length =101, null=True, blank=True)
    manager_approval = models.CharField(max_length =50, null=True, blank=True)
    manager_approval_crm = models.CharField(max_length =50, null=True, blank=True)
    veriification_cfo = models.CharField(max_length =50, null=True, blank=True)
    completely_verified = models.CharField(max_length =50, null=True, blank=True)
    paid = models.CharField(max_length =50, null=True, blank=True)
    is_comission = models.BooleanField(default = False)
    created_at = models.CharField(max_length =50, null=True, blank=True)

    def __str__(self):
        return f"{self.email}"
    
class Deleted_Daily_lead(models.Model):
    crm_id = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length = 101, null=True, blank=True)
    product = models.CharField(max_length = 101, null=True, blank=True)
    plan = models.CharField(max_length = 101, null=True, blank=True)
    renewal = models.CharField(max_length = 101, null=True, blank=True)
    is_exam_fee = models.CharField(max_length = 101, null=True, blank=True)
    amount = models.CharField(max_length = 101, null=True, blank=True)
    source = models.CharField(max_length = 101, null=True, blank=True)
    lead_creator = models.CharField(max_length =101, null=True, blank=True)
    manager_approval = models.CharField(max_length =50, null=True, blank=True)
    manager_approval_crm = models.CharField(max_length =50, null=True, blank=True)
    veriification_cfo = models.CharField(max_length =50, null=True, blank=True)
    support = models.CharField(max_length =50, null=True, blank=True)
    completely_verified = models.CharField(max_length =50, null=True, blank=True)
    paid = models.CharField(max_length =50, null=True, blank=True)
    is_comission = models.BooleanField(default = True)
    created_at = models.CharField(max_length =50, null=True, blank=True)

    def __str__(self):
        return f"{self.email}"
class Deleted_Daily_Sales_Support(models.Model):
    crm_id = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length = 101, null=True, blank=True)
    product = models.CharField(max_length = 101, null=True, blank=True)
    plan = models.CharField(max_length = 101, null=True, blank=True)
    is_exam_fee = models.CharField(max_length = 101, null=True, blank=True)
    amount = models.CharField(max_length = 101, null=True, blank=True)
    source = models.CharField(max_length = 101, null=True, blank=True)
    lead_creator = models.CharField(max_length =101, null=True, blank=True)
    manager_approval = models.CharField(max_length =50, null=True, blank=True)
    manager_approval_crm = models.CharField(max_length =50, null=True, blank=True)
    veriification_cfo = models.CharField(max_length =50, null=True, blank=True)
    completely_verified = models.CharField(max_length =50, null=True, blank=True)
    paid = models.CharField(max_length =50, null=True, blank=True)
    is_comission = models.BooleanField(default = True)
    created_at = models.CharField(max_length =50, null=True, blank=True)

    def __str__(self):
        return f"{self.email}"