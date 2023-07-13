from django.db import models

# Create your models here.
class AffiliateUser(models.Model):
    source_id = models.CharField(max_length=100 , null=True , blank=True)
    username = models.CharField(max_length=100 , null=True , blank=True)
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100 , null=True , blank=True)
    address = models.CharField(max_length=100 , null=True , blank=True)
    country = models.CharField(max_length=100 , null=True , blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True,null=True , blank=True)
    language = models.CharField(max_length=100 , null=True , blank=True)
    referral_code = models.CharField(max_length=100 , null=True , blank=True)
    category_id = models.BigIntegerField(null=True,blank=True)
    accept_aggrement = models.BooleanField(default=False)
    erp_lead_id = models.CharField(max_length=255,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True , blank=True)
    
    def __str__(self):
        return f"{self.email}"
    
    class Meta:
        verbose_name_plural = "AffiliateUsers"



class AffiliateUniqueClick(models.Model):
    source_id = models.CharField(max_length=100 , null=True , blank=True)
    ip = models.CharField(max_length=100 , null=True , blank=True)
    page_url = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    affiliate_id = models.ForeignKey(AffiliateUser, on_delete=models.SET_NULL, null=True, related_name="user_clicks")
    pkr_price = models.IntegerField(default=0)
    usd_price = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.ip}"
    
    class Meta:
        verbose_name_plural = "AffiliateUniqueClicks"