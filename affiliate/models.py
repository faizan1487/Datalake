from django.db import models
from datetime import datetime
# Create your models here.
class AffiliateUser(models.Model):
    email = models.EmailField(unique=True)
    source_id = models.CharField(max_length=100 , null=True , blank=True)
    username = models.CharField(max_length=100 , null=True , blank=True)
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    address = models.CharField(max_length=100 , null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    language = models.CharField(max_length=100 , null=True , blank=True)
    referral_code = models.CharField(max_length=100 , null=True , blank=True)
    category_id = models.BigIntegerField(null=True,blank=True)
    accept_aggrement = models.BooleanField(default=False)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        verbose_name_plural = "AffiliateUsers"


class AffiliateLead(models.Model):
    affiliate = models.ForeignKey(AffiliateUser, on_delete=models.SET_NULL, null=True, related_name="affiliate_leads")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(null=True , blank=True)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return f"{self.email}"


class AffiliateUniqueClick(models.Model):
    ip = models.CharField(max_length=100, unique=True)
    page_url = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    affiliate = models.ForeignKey(AffiliateUser, on_delete=models.SET_NULL, null=True, related_name="affiliate_clicks")
    pkr_price = models.IntegerField(default=0)
    usd_price = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.ip}"
    
    class Meta:
        verbose_name_plural = "AffiliateUniqueClicks"


class Commission(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    affiliate = models.ForeignKey(AffiliateUser, on_delete=models.SET_NULL, null=True, related_name="affiliate_commission")
    product = models.CharField(max_length=200,null=True,blank=True)
    source = models.CharField(max_length=200,null=True,blank=True)
    amount_pkr = models.IntegerField(default=0)
    amount_usd = models.IntegerField(default=0)
    commission_usd = models.CharField(max_length=30, default=0)
    commission_pkr = models.CharField(max_length=30, default=0)
    student_email = models.CharField(max_length=150)
    date = models.DateTimeField(default=datetime.now)
    is_paid = models.BooleanField(default=False)
    created_at= models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.product}"